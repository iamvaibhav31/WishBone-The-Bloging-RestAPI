import random
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import (post_save , post_delete)


## UTILS



def generate_unique_id(text):
    Choices = list(str(text))
    while True:
        gen_code = "".join(random.choices(Choices , k=len(Choices)//2))
        if post.objects.filter(id = gen_code).count() == 0:
            break
    
    return gen_code



## MODELS



class post(models.Model):

    class Categories(models.TextChoices):
        World = "World"
        Enviroment = "Enviroment"
        Technology = "Technology"
        Design = "Design"
        Culture = "Culture"
        Business = "Business"
        Politics = "Politics"
        Opinion = "Opinion"
        Science = "Science"
        Health = "Health"
        Style = "Style"
        Travel = "Travel"
    
    class Status(models.TextChoices):
        PUBLISHED = "PUBLISHED"
        DRAFT = "DRAFT"
    
    id = models.CharField( max_length=250 , primary_key=True ,blank=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    thumbnail_url = models.ImageField(upload_to='thubnail_images',blank=True)
    title = models.CharField(max_length=200 , blank=True)
    categories = models.CharField(max_length=30 , choices=Categories.choices , default=Categories.World)
    excerpt = models.TextField(blank=True)
    status = models.CharField(max_length=30 , choices=Status.choices , default=Status.PUBLISHED)
    content = models.TextField(blank=True) 
    pinned = models.BooleanField(default=False)
    publish_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def thubnail(self):
    #     return self.thubnail.url

    class Meta:
        ordering = ['-publish_at']

    def save(self,*args , **kwargs ):
        author = str(self.author)
        if not self.id:
            text = f"{author.capitalize()}-BlogPost-{self.title}-Count-{post.objects.all().filter(author=self.author).count()}"
            print(text)
            self.id = generate_unique_id(text)
        return super(post , self).save(*args , **kwargs)

    def __str__(self):
        return self.id

#!!_____________________________________________________________!!#

class postAchivements(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    veiws = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.id

#!!_____________________________________________________________!!#

class comments(models.Model):
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)
    #  models.ManyToManyField(post, verbose_name='post_id' , on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    comment = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.post_id)


# class CommentAchivement(models.Model):




## SIGNALS


@receiver(post_save , sender = post)
def create_postachiver(sender , instance , created , *args , **kwargs):
    if created :
        obj_post_achiver = postAchivements(id=instance.id)
        obj_post_achiver.save()


@receiver(post_delete , sender = post)
def create_postachiver(sender , instance , *args , **kwargs):
    postAchivements.objects.get(id=instance.id).delete()


@receiver(post_save , sender = comments)
def create_postachiver(sender , instance , created , *args , **kwargs):
    if created :
        obj_post_achiver = postAchivements.objects.get(id=instance.post_id)
        obj_post_achiver.comment = comments.objects.filter(post_id = instance.post_id).count()
        obj_post_achiver.save()


