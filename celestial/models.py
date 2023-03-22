from django.db import models
from datetime import date, datetime, timedelta 
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import User
from typing import Any
from django.db import models
from celestial.managers import *

'''
POST MDOELS: ===================================================================================
'''

class Post(models.Model):
    user: Any = models.ForeignKey('UserProfile', default=1, null=True, on_delete=models.SET_DEFAULT, related_name="posts")
    shown_name: str = models.CharField(max_length=100, default=None)
    topic: Any = models.ForeignKey('Topic', on_delete=models.SET_DEFAULT, default=0)
    prompt: str = models.TextField(default="Create a post.")
    n_prompt: str = models.TextField(null=True, blank=True)
    uploaded_image: str = models.UUIDField(null=True, default=None, editable=False)
    generated_images: str = models.TextField(default = '{}')
    image: str = models.CharField(max_length=100, null=True, default=None)
    draft: bool = models.BooleanField(default=True)
    published_on: date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    like_count: int = models.IntegerField(default=1)
    dislike_count: int = models.IntegerField(default=0)
    score: int = models.FloatField(default=0)
    magic: int = models.IntegerField(default=0)
    interacted: str = models.TextField(default = '{}')
    updated: datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = models.Manager()
    
    class Meta:
        verbose_name: str = "post"
        verbose_name_plural: str = "posts"
        ordering: list = ["-published_on", "prompt"]

    def __str__(self) -> str:
        return f"{self.prompt}"
    
    def on_post_intract(self,is_like:bool):
        self.add_like() if is_like else self.add_dislike
        self.save()

    def add_like(self):
        like_count = self.like_count
        self.like_count = like_count + 1
        self.update_post_score()
        
    def add_dislike(self):
        dislike_count = self.dislike_count
        self.dislike_count = dislike_count + 1
        self.update_post_score()

    def update_post_score(self):
        liked_count = self.like_count
        disliked_count = self.dislike_count
        if liked_count + disliked_count == 0:
            score = 0
        else:
            score = (liked_count - disliked_count) / (liked_count + disliked_count)
        self.score = score
    
    def get_interacted(self): return json.loads(self.interacted)
    def set_interacted(self,value): self.interacted = json.dumps(value)

    def get_generated_images(self): return json.loads(self.generated_images)
    def set_generated_images(self,value): self.generated_images = json.dumps(value)



'''
TOPIC MDOELS: ===================================================================================
'''
#TODO: topic get list of titles. with just one start_on
class Topic (models.Model):
    title: str = models.CharField(max_length=250, default=None)
    description: str = models.CharField(max_length=250, default=None)
    created_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    starts_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    finished_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    active: bool = models.BooleanField(default = False)
    
    objects = models.Manager()

    class Meta:
        verbose_name: str = "title"
        verbose_name_plural: str = "titles"
        ordering: list = ["-starts_on", "title"]

    def __str__(self) -> str:
        return f"{self.title}"
    def set_finished_on(self):
        self.finished_on = self.starts_on + timedelta(days = 7)

'''
USER PROFILE MDOELS: ============================================================================
'''


class UserProfile(models.Model):
    user: Any = models.OneToOneField(User, on_delete=models.CASCADE)
    shown_name: str = models.CharField(max_length=100, null=False)
    interacted = models.TextField(default = '{}', null=True)
    myPosts: str = models.TextField(default = '{}', null=True)
    device_id: str = models.CharField(max_length=100, null=False, default='0')
    objects = models.Manager()

    class Meta:
        verbose_name: str = "shown_name"
        verbose_name_plural: str = "shown_names"
        ordering: list = ["shown_name"]

    def __str__(self) -> str:
        return f"{self.shown_name}"

    def set_interacts(self, value):
        self.interacted = json.dumps(value)

    def get_interacts(self):
        if self.interacted is None:
            return None
        else:
            return json.loads(self.interacted)

    def set_myPosts(self, value):
        self.myPosts = json.dumps(value)

    def get_myPosts(self):
        if self.myPosts is None:
            return None
        else:
            return json.loads(self.myPosts)
    

'''
QUEUE MDOELS: ===================================================================================
'''

class ScoreQueue(models.Model):
    post: Any = models.OneToOneField(Post, on_delete=models.CASCADE, default=0)
    update_date: datetime = models.DateTimeField(null=False, auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True
        ordering: list = ["update_date"]     

class HighScoreQueue(ScoreQueue):
    pass

class MidScoreQueue(ScoreQueue):
    pass

class LowScoreQueue(ScoreQueue):
    pass
    
class configs(models.Model):
    key: str = models.CharField(max_length=100, null=False)
    value: str = models.CharField(max_length=100, null=True)