from typing import Tuple
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.expressions import F
from django.core.signing import Signer
signer = Signer()
from autoslug import AutoSlugField


GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)

class User(AbstractUser):
    gender = models.CharField(max_length=15, choices=GENDER, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)

    def full_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def getEncryptedID(self):
        value = signer.sign(self.id)
        return value

    def getUnsignID(self):
        return signer.unsign(self.getEncryptedID())

    class Meta(object):
        unique_together = ('email',)

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = AutoSlugField(populate_from='title')
    content = models.TextField(null=False, blank=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_blogs")

    def __str__(self):
        return self.title

    def author(self):
        return self.posted_by.full_name()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    content = models.TextField(null=False, blank=False)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_comments")

    def author(self):
        return self.comment_by.full_name()

