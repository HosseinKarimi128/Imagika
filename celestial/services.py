import random
from typing import Tuple
from django.contrib.auth.models import User
from httpx import Auth
from celestial.models import *
from celestial.schema import *
from asgiref.sync import sync_to_async
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.db.models import Q

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
        return UserOutLogin(
            device_id = user.device_id,
            shown_name = user.shown_name,
            token =  access_token,
            refresh_token = refresh_token,
            posts = user.get_myPosts(),
            interacts = user.get_interacts()
        )
    
#SERVICE ===
@sync_to_async
def on_get_profile(device_id) -> UserProfileOut:
    user = UserProfile.objects.get(device_id = device_id)
    return UserProfileOut(
        device_id = user.device_id,
        shown_name = user.shown_name,
        posts = user.get_myPosts(),
        interacts = user.get_interacts())

#SERVICE ===
async def on_get_timeline(user:UserProfile) -> TimelineOut:
    hl = await get_nonRepetitious_post_by_qeueu(HighScoreQueue, user,3)
    ml = await get_nonRepetitious_post_by_qeueu(MidScoreQueue, user,5)
    ll = await get_nonRepetitious_post_by_qeueu(LowScoreQueue, user,2)
    list = hl + ml + ll
    random.shuffle(list)
    return TimelineOut(queue = list)

# AXILLARY
@sync_to_async
def get_nonRepetitious_post_by_qeueu(queue:models.Model, user:UserProfile, batch_size: int) -> TimelineOut:
    queue_in = list(queue.objects.order_by('id').all())
    count = len(queue)
    num = 0
    queue_out = []
    while num <= count and len(queue_out) < batch_size:
        item_in = Post.object.get(id = queue_in[num].post_id)
        if validate_nonRepetitious_post(user,item_in):
            num += 1
            continue
        else:
            item = PostOut(
                id = item_in.id,
                shown_name = item_in.shown_name,
                image =  item_in.generated_image
            )
            queue_out.append(item)
            num += 1
    return TimelineOut(queue = queue_out)

# AXILLARY
def validate_nonRepetitious_post(user:UserProfile, post: Post) -> bool:
    post_interacted_users = post.get_interacted()
    return True if str(user.id) in post_interacted_users.keys() else False

#SERVICE ===
@sync_to_async
def on_post_interact_update(user: UserProfile, post_in: PostForInteract) -> None:
    interacted_posts = user.get_interacts()
    post_in_db = Post.objects.get(id = post_in.id)
    if interacted_posts is None:
        interacted_posts = {}
    interacted_posts[post_in.id] = post_in.isLike
    user.set_interacts(interacted_posts)
    if post_in.isLike:
        post_in_db.add_like()
    else:   
        post_in_db.add_dislike()
    post_user_interacts = post_in_db.get_interacted()
    post_user_interacts[user.id] = post_in.isLike
    post_in_db.set_interacted(post_user_interacts)
    with transaction.atomic():
        user.save()
        post_in_db.save()
#AXILLARY
@sync_to_async
def has_user_interacted(user: UserProfile, post: Post) -> bool: 
    interacted_posts = user.get_interacts()
    if interacted_posts is None:
        interacted_posts = {}
    return (str(post.id) in interacted_posts.keys())
#SIGNAL
@receiver(post_save, sender=Post)
def update_queue(sender, instance,**kwargs) -> None:
    before_score = instance.score
    instance.update_post_score()
    after_score = instance.score
    if before_score <= 0.2:
        try:
            LowScoreQueue.objects.get(post_id = instance.id).delete()
        except Exception:
            pass
    elif before_score <= 0.8:
        try:
            MidScoreQueue.objects.get(post_id = instance.id).delete()
        except Exception:
            pass
    else:
        try:
            MidScoreQueue.objects.get(post_id = instance.id).delete()
        except Exception:
            pass
    if after_score <= 0.2:
        LowScoreQueue.objects.create(post_id = instance.id)
    elif after_score <= 0.8:
        MidScoreQueue.objects.create(post_id = instance.id)
    else:
        HighScoreQueue.objects.create(post_id = instance.id)

'''
POST SERVICES ==========================================================
'''

#SERVICE ===
@sync_to_async
def on_get_topic() -> TopicOutList:
    topics  = list(Topic.objects.filter(Q(active = True)).values('id','title'))
    return TopicOutList(items=topics)

#SERVICE ===
@sync_to_async
def on_create_post(user_post: UserInCreatePost) -> PostOut:
    generated_images = geterate_image(prompt = user_post.prompt,
                                           n_prompt = user_post.n_prompt,
                                           image = user_post.image_id)
    post = Post.objects.create(
        user_id = user_post.user_id,
        shown_name = user_post.shown_name,
        topic_id = user_post.topic,
        prompt=user_post.prompt,
        n_prompt = user_post.n_prompt,
        uploaded_image = user_post.image_id,
        generated_image = generated_images)
    return PostOut(id = post.id, shown_name = post.shown_name, image = post.generated_image)
#SIGNAL
@receiver(post_save, sender=Post)
def put_post_in_queue(sender, instance, created, **kwargs) -> None:
    if created and instance.topic_id != 0:
        HighScoreQueue.objects.create(post_id=instance.id)

#APP CALL
def geterate_image(post:PostForDaVinchi) -> PostFromDaVinchi:
    # talking with DaVinchi
    generated_images_list = []
    #this generated_images_list is temporal and should be changed after DaVinchi Creation
    generated_images_list.append(post.image)
    generated_images_list.append(post.image)
    return PostFromDaVinchi(images = generated_images_list)

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
        starts_on = admin_topic.starts_on)
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
