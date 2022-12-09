from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import ContentSerializer, UserSerializer, NewsSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core import serializers



# ---------------@api_view 이용
# 최신 뉴스 리스트 출력
@api_view(['GET'])
def RecentNews(request):
    json_dumps_params = {'ensure_ascii': False}
    sql = "select * from tb_news where DATE_FORMAT(WritedAt ,'%%Y-%%m-%%d')='2022-11-30' group by SubCategory order by id desc"
    obj = TbNews.objects.raw(sql)
    result_list = []

    data_list = serializers.serialize("python", obj)
    for data in data_list:
        result_list.append(data.get('fields'))

    return JsonResponse(result_list[:10], json_dumps_params=json_dumps_params, safe=False)

@api_view(['GET'])
def Recent(request):

    if request.method =='GET':
        content = TbNews.objects.order_by('subcategory', 'writedat').distinct('subcategory') 
        serializer = NewsSerializer(content,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#전체 리스트 보여주는 뷰(get, post만 사용)
@api_view(['GET', 'POST'])
def ContentsList(request):
    if request.method =='GET':
        content = get_list_or_404(TbContentrec)[:20]
        serializer = ContentSerializer(content, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#news_pk값 받아서 news_id 값에 해당하는 데이터만 디테일하게 보여주는 뷰 (get, put, delete 사용)
@api_view(['GET', 'PUT', 'DELETE'])
def ContentsNewsDetail(request, news_pk):
    try:
        content = get_object_or_404(TbContentrec, newsid=news_pk)
    except TbContentrec.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Detail Get
    if request.method =='GET':
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #update
    elif request.method =='PUT':
        serializer = ContentSerializer(content, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    elif request.method == 'DELETE':
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ContentsNewsFind(request, news_id):
    try:
        news = get_object_or_404(TbNews, id=news_id)
    except TbContentrec.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    # Detail Get
    if request.method =='GET':
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ContentsRecNews(request, recnews_id):
    if request.method =='GET':
        rec = TbContentrec.objects.get(newsid=recnews_id)
        recnews = TbNews.objects.filter(id__in=[rec.r1, rec.r2,rec.r3, rec.r4, rec.r5])

        serializer = NewsSerializer(recnews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def UsersRecNews(request, user_id):
#     if request.method =='GET':
#         rec = UserNews.objects.get(newsid=user_id)
#         recnews = TbNews.objects.filter(id__in=[rec.r1, rec.r2,rec.r3, rec.r4, rec.r5])

#         serializer = NewsSerializer(recnews, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


