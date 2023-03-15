import random
from typing import Tuple
from django.contrib.auth.models import User
from core.models import *
from core.schema import *
from asgiref.sync import sync_to_async
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

'''
USER SERVICES ==========================================================
'''
#TODO change the name of the services 
#TODO set schema for all services output
#TODO sort services in a logical order
#TODO set functions return hints

def get_user_by_username(username = str):
    return UserProfile.objects.get(device_id=username)

@sync_to_async
def get_user_by_username_async(username = str):
    return User.objects.get(username=username)

@sync_to_async
def create_user(device_id: str, email: str):
    _username = email.split('@')[0]
    return User.objects.create(username = device_id, email = email, first_name = _username)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, shown_name = instance.first_name, device_id = instance.username)

@sync_to_async
def get_my_posts(user:UserProfile):
    posts = user.get_myPosts()
    if posts is None:
        posts = {}
    return posts

@sync_to_async
def on_user_delete(device_id:int) -> None:
    User.objects.get(device_id = device_id).delete()

'''
POST SERVICES ==========================================================
'''

@sync_to_async
def create_post(request, user:UserProfile):
    post = Post.objects.create(user_id = user.id,
                        shown_name = user.shown_name,
                        topic_id = request.topic,
                        prompt=request.prompt,
                        n_prompt = request.n_prompt,
                        uploaded_image = request.uploaded_image)
    return post.__dict__

@sync_to_async
def get_post_by_id(post_id: int):
    return Post.objects.get(id=post_id)

@sync_to_async
def has_user_interacted(user: UserProfile, post: Post) -> bool: 
    interacted_posts = user.get_interacts()
    if interacted_posts is None:
        interacted_posts = {}
    return (str(post.id) in interacted_posts.keys())

@sync_to_async
def on_post_intract_update(user: UserProfile, post: Post, isLike: bool) -> None:
    interacted_posts = user.get_interacts()
    if interacted_posts is None:
        interacted_posts = {}
    interacted_posts[post.id] = isLike
    user.set_interacts(interacted_posts)
    if isLike:
        post.add_like()
    else:   
        post.add_dislike()
    post_user_interacts = post.get_interacted()
    post_user_interacts[user.id] = isLike
    post.set_interacted(post_user_interacts)
    with transaction.atomic():
        user.save()
        post.save()

@receiver(post_save, sender=Post)
def put_post_in_queue(sender, instance, created, **kwargs):
    if created:
        HighScoreQueue.objects.create(post_id=instance.id)


@sync_to_async
def on_delete_post(post_id: int):
    Post.objects.get(id=post_id).delete()
'''
TOPIC SERVICES ==========================================================
'''

@sync_to_async
def create_topic(title: str):
    topic = Topic.objects.create(title=title)
    return topic.__dict__

@sync_to_async
def on_delete_topic(topic_id):
    Topic.objects.get(id = topic_id).delete()

'''
QUEUE SERVICES ===========================================================
'''
async def get_user_queue(user:UserProfile) -> QueueOut:
    hl = await get_nonRepetitious_post_by_qeueu(HighScoreQueue, user,3)
    ml = await get_nonRepetitious_post_by_qeueu(MidScoreQueue, user,5)
    ll = await get_nonRepetitious_post_by_qeueu(LowScoreQueue, user,2)
    list = hl + ml + ll
    random.shuffle(list)
    posts = map(int, list)
    q_posts = await aggregate(posts,user)
    return QueueOut(queue = q_posts, count = len(q_posts))

@sync_to_async
def get_nonRepetitious_post_by_qeueu(queue:models.Model, user:UserProfile, batch_size: int):
    count = queue.objects.all().count()
    num = 0
    q = []
    while num <= count and len(q) < batch_size:
        first_queue_post = num*batch_size
        last_queue_post = first_queue_post+batch_size
        q = q + list(queue.objects.order_by('id').values_list('post_id', flat=True)[first_queue_post:last_queue_post])
        for post_id in q:
            post = Post.objects.get(id=post_id)
            if validate_nonRepetitious_post(user,post):
                q.remove(post_id) 
        num += 1
    return q

"""
@sync_to_async
def get_queue_low(user:User, post:Post):
    num = 0
    while True:
        num =+ 1
        first_queue_post = num*2
        last_queue_post = first_queue_post+1
        queue = LowScoreQueue.objects.order_by('id')[first_queue_post:last_queue_post].post_id
        for post_id in queue:
            post = Post.objects.get(id=post_id)
            if validate_nonRepetitious_post(user,post):
                queue.remove(post) 
        if len(queue) >= 2:
            break
    return list(queue)

@sync_to_async
def get_queue_mid(user:User, post:Post):
    num = 0
    while True:
        num =+ 1
        first_queue_post = num*5
        last_queue_post = first_queue_post+1
        queue = MidScoreQueue.objects.order_by('id')[first_queue_post:last_queue_post].post_id
        for post in queue:
            if validate_nonRepetitious_post(user,post):
                queue.remove(post) 
        if len(queue) >= 5:
            break
    return list(queue)

@sync_to_async
def get_queue_high(user:User, post:Post):
    num = 0
    while True:
        num =+ 1
        first_queue_post = num*3
        last_queue_post = first_queue_post+1
        queue = HighScoreQueue.objects.order_by('id')[first_queue_post:last_queue_post].post_id
        for post in queue:
            if validate_nonRepetitious_post(user,post):
                queue.remove(post) 
        if len(queue) >= 3:
            break
    return list(queue)
"""


def validate_nonRepetitious_post(user:UserProfile, post: Post):
    post_interacted_users = post.get_interacted()
    return True if str(user.id) in post_interacted_users.keys() else False

@sync_to_async
def aggregate(posts:List[Post],user:User) -> List[models.QuerySet]:
    res = Post.objects.filter(id__in=posts)
    q = [QueueItem(device_id = user.device_id, shown_name = user.shown_name,
                     post_id = post.id, image = post.generated_image) for post in res]
    return q

