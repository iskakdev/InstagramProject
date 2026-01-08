from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    bio = models.TextField()
    user_image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_official = models.BooleanField(default=False)
    user_link = models.URLField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def followings(self):
        following = self.following_user.all()
        return following.count()

    def followers(self):
        follower = self.follower_user.all()
        return follower.count()

    def posts(self):
        post = self.user_post.all()
        return post.count()


class Follow(models.Model):
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_user')
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_user')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('following', 'follower')


class Post(models.Model):
    description = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='user_post')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.description}, {self.hashtag}'

    def likes(self):
        like = self.like_post.all()
        return like.count()


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='content_post')
    post_content = models.FileField()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comment')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return  f'{self.post}, {self.text}'

    def comment_likes(self):
        like = self.like_comment.all()
        return like.count()


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'comment')


class Chat(models.Model):
    persons = models.ManyToManyField(UserProfile)
    create_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)