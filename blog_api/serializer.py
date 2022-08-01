from rest_framework import serializers
from .models import *

class postSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.ImageField(required=True)
    
    class Meta:
        model = post
        fields = '__all__'
        # feilds = ('id' ,'author' , 'thumbnail_url' , 'title' , 'categories' , 'excerpt' , 'status' , 'content',"created_at")
        # exclude = ('publish_at',"thumbnail" )
    
    
    def get_thumbnail_url(self, post):
        request = self.context.get('request')
        thumbnail_url = post.thumbnail_url.url
        return request.build_absolute_uri(thumbnail_url)
    



class postachivementSerializer(serializers.ModelSerializer):
    class Meta:
        model = postAchivements
        fields = '__all__'



class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        exclude = [
            'created_on','author',"post_id"
        ]
        