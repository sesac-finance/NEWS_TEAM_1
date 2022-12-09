from rest_framework import serializers
from .models import TbContentrec, UserNews, TbNews

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TbContentrec
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNews
        fields = ('__all__')

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbNews
        fields = ('__all__')
