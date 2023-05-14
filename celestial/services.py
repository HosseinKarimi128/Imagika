import logging
import random
from typing import Tuple
from django.contrib.auth.models import User
from celestial.auth import Auth
from celestial.models import *
from celestial.schema import *
from asgiref.sync import sync_to_async
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.db.models import Q


logger = logging.getLogger(__name__)
#TODO set the constants using config table
'''
USER SERVICES ==========================================================
'''
#SERVICE ===
@sync_to_async
def on_signup(user:UserInSignUp) -> None:
    shown_name = user.email.split('@')[0]
    User.objects.create(username = user.device_id, email = user.email, first_name = shown_name)
# SIGNAL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs) -> None:
    if created:
        UserProfile.objects.create(user=instance, shown_name = instance.first_name, device_id = instance.username)

#SERVICE ===
@sync_to_async
def on_user_login(user: UserInLogin) -> UserOutLogin:
    user_existed = False
    try: 
        user = UserProfile.objects.get(device_id = user.device_id)
        user_existed =True
    except:
        return user_existed
    if user_existed:
        auth_handler = Auth()
        access_token = auth_handler.encode_token(user.device_id)
        refresh_token = auth_handler.encode_refresh_token(user.device_id)
        user_posts = list(Post.objects.filter(user_id=user.id).values())
        return UserOutLogin(
            device_id = user.device_id,
            shown_name = user.shown_name,
            posts = user_posts,
            token =  access_token,
            refresh_token = refresh_token,
        )
    
#SERVICE ===
@sync_to_async
def on_get_profile(device_id) -> UserProfileOut:
    user = UserProfile.objects.get(device_id = device_id)
    user_posts = list(Post.objects.filter(user_id=user.id).values())
    logger.info('='*100)
    logger.info(user_posts)
    logger.info('='*100)
    return UserProfileOut(
        device_id = user.device_id,
        shown_name = user.shown_name,
        posts = user_posts,
        interacts = dict(user.interacted.values()),
        magic = user.magic)

#SERVICE ===
async def on_get_timeline(user:UserProfileOut) -> TimelineOut:
    hl = await get_nonRepetitious_post_by_qeueu(HighScoreQueue, user,3)
    ml = await get_nonRepetitious_post_by_qeueu(MidScoreQueue, user,5)
    ll = await get_nonRepetitious_post_by_qeueu(LowScoreQueue, user,2)
    list_out = list(hl) + list(ml) + list(ll)
    random.shuffle(list_out)
    return TimelineOut(queue = list_out)

# AXILLARY
@sync_to_async
def get_nonRepetitious_post_by_qeueu(queue:models.Model, user:UserProfileOut, batch_size: int) -> TimelineOut:
	user_in_db = UserProfile.objects.get(device_id =user.device_id)
	queue_in = list(queue.objects.order_by('id').all())
	count = len(queue_in)
	if count == 0: return []
	num = 0
	queue_out = []
	while num < count and len(queue_out) < batch_size:
		item_in = Post.objects.get(id = queue_in[num].post_id)
		if has_user_interacted(user_in_db,item_in):
			continue
		else:
			item = PostPublishOut(id = item_in.id, shown_name = item_in.shown_name, image =  item_in.image)
			queue_out.append(item)
			num += 1
	return TimelineOut(queue = queue_out).__dict__["queue"]

#SERVICE ===
@sync_to_async
def on_post_interact_update(user: UserProfileOut, post_in: PostForInteract) -> None:
    user_in_db = UserProfile.objects.get(device_id = user.device_id)
    post_in_db = Post.objects.get(id = post_in.id)
    post_in_db.interacted.add(user_in_db)
    user_in_db.interacted.add(post_in_db)
    post_in_db.add_like() if post_in.isLike else post_in_db.add_dislike()
    with transaction.atomic():
        user_in_db.save(update_fields=['interacted'])
        post_in_db.save(update_fields=['like_count','dislike_count','interacted','score'])
#TODO
#AXILLARY
@sync_to_async
def has_user_interacted(user: UserProfileOut, post: Post) -> bool: 
    user_in_db = UserProfile.objects.get(device_id = user.device_id)
    post_in_db = Post.objects.get(id=post.id)
    return (user_in_db.interacted.filter(id=post_in_db.id).exists())

#SERVICE OUT ===
def update_queue() -> None:
    posts = Post.objects.filter(draft = False).all()    
    for post in posts:
        #remove post from old queue
        try:
            LowScoreQueue.objects.get(post_id = post.id).delete()
        except Exception: pass
        try:
            MidScoreQueue.objects.get(post_id = post.id).delete()
        except Exception: pass
        try:
            HighScoreQueue.objects.get(post_id = post.id).delete()
        except Exception: pass
        
        # add post to it's new queue
        if post.score <= -0.4:
            LowScoreQueue.objects.create(post_id = post.id)
        elif post.score <= 0.4:
            MidScoreQueue.objects.create(post_id = post.id)
        else:
            HighScoreQueue.objects.create(post_id = post.id)
'''
POST SERVICES ==========================================================
'''

#SERVICE ===
@sync_to_async
def on_get_topic() -> TopicOutList:
    topics  = list(Topic.objects.filter(Q(active = True)).values('id','title','description'))
    return TopicOutList(items=topics)

#SERVICE ===
@sync_to_async
def on_create_post(user_post: UserInCreatePost) -> PostOut:
    user = UserProfile.objects.get(device_id = user_post.user_device_id)
    post_for_davinchi = PostForDaVinchi(prompt = user_post.prompt,
                                           n_prompt = user_post.n_prompt,
                                           image = user_post.image_id)
    
    generated_images = generate_images(post_for_davinchi)
    generated_images_list = []
    for image in generated_images.images: generated_images_list.append(image) 
    post = Post(
        user_id = user.id,
        shown_name = user.shown_name,
        topic_id = user_post.topic_id,
        prompt=user_post.prompt,
        n_prompt = user_post.n_prompt,
        uploaded_image = user_post.image_id)
    post.generated_images = generated_images_list
    post.save()
    return PostOut(id = post.id, shown_name = post.shown_name, images = post.generated_images)


#APP CALL
def generate_images(post:PostForDaVinchi) -> PostFromDaVinchi:
    # talking with DaVinchi
    generated_images = []
    #this generated_images_list is temporal and should be changed after DaVinchi Creation
    generated_images.append(post.image)
    generated_images.append(post.image)
    return PostFromDaVinchi(images = generated_images)

#SERVICE ===
@sync_to_async
def on_publish_post(post:PostForPublish) -> PostPublishOut:
    post_out = Post.objects.get(id = post.id)
    post_out.draft = False
    post_out.published_on = datetime.now()
    post_out.image = post_out.generated_images[post.image_number]
    post_out.save(update_fields=['image', 'draft','published_on'])
    return PostPublishOut(
        id = post_out.id,
        shown_name = post_out.shown_name,
        image = post_out.image
    )
# SIGNAL
@receiver(post_save, sender=Post)
def put_post_in_queue(sender, instance, created, update_fields, **kwargs) -> None:
    if not created and instance.topic_id != 0 and (
        update_fields and
        'draft' in update_fields
    ):
        MidScoreQueue.objects.create(post_id=instance.id)

#SERVICE ===
@sync_to_async
def on_delete_post(post_id: int) -> None:
    Post.objects.get(id=post_id).delete()
'''
TOPIC SERVICES ==========================================================
'''

#SERVICE ===
@sync_to_async
def on_create_topic(admin_topic: AdminInCreateTopic) -> TopicOutInCreate:
    topic = Topic.objects.create(
        title=admin_topic.title,
        starts_on = admin_topic.starts_on,
        description = admin_topic.description)
    topic.set_finished_on()
    return TopicOutInCreate(
        id = topic.id,
        title = topic.title,
        start_date = topic.starts_on,
        end_date = topic.finished_on)

#SERVICE ===
@sync_to_async
def on_delete_topic(topic_id) -> None:
    Topic.objects.get(id = topic_id).delete()
