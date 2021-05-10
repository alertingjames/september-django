import datetime
import difflib
import string
from itertools import islice

import xlrd
import re
from django.core import mail
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
from _mysql_exceptions import DataError, IntegrityError
from django.template import RequestContext

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
import json
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from xlrd import XLRDError
from time import gmtime, strftime

from september.serializers import MemberSerializer, ProductSerializer
from .models import Member, Product
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django import forms
import sys

def index(request):
    return HttpResponse("Hello! This is September.")


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def register_user(request):

    if request.method == 'POST':

        eml = request.POST.get('email', None)
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        phone = request.POST.get('phone', None)

        users = Member.objects.filter(email=eml)
        count = users.count()

        if count ==0:

            user = Member()
            user.email = eml
            user.name = name
            user.password = password
            user.phone_number = phone

            user.save()

            user1 = User()
            user1.username = eml
            user1.email = eml
            user1.password = password
            user1.set_password(password)
            user1.save()

            user1 = authenticate(username=eml, password=password)
            login(request,user1)

            resp = {'result': '0', 'user_id': user.pk}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:

            resp_er = {'result': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login_from_app(request):

    if request.method == 'POST':

        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user0 = Member.objects.filter(email=email, password=password)
        count = user0.count()
        if count>0:

            user = authenticate(username=email, password=password)
            login(request, user)

            serializer = MemberSerializer(user0, many=True)
            resp = {'result': '0', 'user_info': serializer.data}

            return JsonResponse(resp, status=status.HTTP_200_OK)
        else:
            resp = {'result': '1'}
            return JsonResponse(resp)


    elif request.method == 'GET':

        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def upload_product_image(request):

    if request.method == 'POST':

        image = request.FILES['file']

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        product.image_url = "http://18.220.226.218:9000"+ uploaded_file_url
        product.save()

        resp = {'result': '0'}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


    elif request.method == 'GET':

        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def add_product(request):

    if request.method == 'POST':

        email = request.POST.get('email', None)
        keyword = request.POST.get('keyword', None)
        title = request.POST.get('title', None)
        brand = request.POST.get('brand', None)
        gender = request.POST.get('gender', None)
        price = request.POST.get('price', None)
        category = request.POST.get('category', None)
        seller = request.POST.get('seller', None)
        description = request.POST.get('description', None)

        member=Member.objects.get(email=email)
        user_id=str(member.id)

        product = Product()
        product.user_id = user_id
        product.title = title
        product.brand = brand
        product.gender = gender
        product.price = price
        product.category = category
        # if "$" in price:
        #     product.price = price
        # else:
        #     product.itemPrice = "$" + str(price)
        product.sale_url = seller
        product.description = description
        product.keyword=keyword

        product.save()

        resp = {'result': '0','product_id': product.id}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def get_products(request):

    if request.method == 'POST':

        email = request.POST.get('email', None)

        member = Member.objects.get(email=email)
        user_id = member.id

        products = Product.objects.filter(user_id=user_id)
        serializer = ProductSerializer(products, many=True)
        resp = {'result': '0', 'product_info': serializer.data}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':

        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def update_product(request):

    if request.method == 'POST':

        product_id = request.POST.get('product_id', None)
        keyword = request.POST.get('keyword', None)
        title = request.POST.get('title', None)
        brand = request.POST.get('brand', None)
        gender = request.POST.get('gender', None)
        price = request.POST.get('price', None)
        category = request.POST.get('category', None)
        seller = request.POST.get('seller', None)
        description = request.POST.get('description', None)

        product = Product.objects.get(id=product_id)
        product.title = title
        product.brand = brand
        product.gender = gender
        product.price = price
        product.category = category
        # if "$" in price:
        #     product.price = price
        # else:
        #     product.itemPrice = "$" + str(price)
        product.sale_url = seller
        product.description = description
        product.keyword=keyword

        product.save()

        resp = {'result': '0'}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delete_product(request):

    if request.method == 'POST':

        product_id = request.POST.get('product_id', None)

        Product.objects.filter(id=product_id).delete()

        resp = {'result': '0'}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def get_similar_products(request):

    if request.method == 'POST':

        keyword = request.POST.get('keyword', None)
        list=[]
        threshold_ratio=0.6

        products = Product.objects.all()

        for product in products:
            ratio = difflib.SequenceMatcher(None, product.keyword, keyword).ratio()
            if (ratio > threshold_ratio):
                list.append(product)

        serializer = ProductSerializer(list, many=True)
        resp = {'result': '0', 'product_info': serializer.data}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':

        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def get_member_info(request):

    if request.method == 'POST':

        user_id = request.POST.get('user_id', None)

        member = Member.objects.filter(id=user_id)

        serializer = MemberSerializer(member, many=True)
        resp = {'result': '0', 'user_info': serializer.data}

        return JsonResponse(resp, status=status.HTTP_200_OK)

    elif request.method == 'GET':

        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def upload_user_photo(request):

    if request.method == 'POST':

        image = request.FILES['file']

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        user_id = request.POST.get('user_id')

        user = Member.objects.get(id=user_id)
        user.photo_url = "http://18.220.226.218:9000"+ uploaded_file_url
        user.save()

        users = Member.objects.filter(id=user_id)
        serializer=MemberSerializer(users, many=True)

        resp = {'result': '0', 'user_info':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


    elif request.method == 'GET':

        pass






















