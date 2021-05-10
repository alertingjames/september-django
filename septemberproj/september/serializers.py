from rest_framework import serializers
from .models import Member, Product

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'password', 'photo_url', 'phone_number')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'user_id', 'title', 'brand', 'image_url', 'gender', 'price', 'category', 'sale_url', 'keyword' , 'description')
