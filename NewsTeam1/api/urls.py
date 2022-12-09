from django.urls import path
from . import views

urlpatterns = [
    path('contents/', views.ContentsList ),  # 추천 아이디 리스트
    path('contents/<int:news_pk>', views.ContentsNewsDetail),  #int에 넣은 값에 해당하는 news_id 데이터만 불러옴
    path('contents/find/<int:news_id>', views.ContentsNewsFind),  #int에 넣은 값에 해당하는 news_id의 news 데이터 전체 불러옴
    path('contents/recnews/<int:recnews_id>', views.ContentsRecNews),  #recnews_id 값에 해당하는 추천 뉴스 리스트의 데이터를 모두 불러옴
    path('recent/', views.RecentNews ),
    #path('recenta/', views.Recent )

    #path('users/recnews/<int:user_id>', views.UsersRecNews),  # userid 기반 협업필터링 추천 뉴스 출력
]


"""
    path('users/', views.UsersList ),  # 추천 아이디 리스트
    path('users/news/<int:news_pk>', views.UsersNewsDetail),  #int에 넣은 값에 해당하는 news_id 데이터만 불러옴
    path('Users/news/find/<int:news_id>', views.UsersNewsFind),  #int에 넣은 값에 해당하는 news_id의 news 데이터 전체 불러옴
    path('Users/recnews/<int:recnews_id>', views.UsersRecNews),  #recnews_id 값에 해당하는 추천 뉴스 리스트의 데이터를 모두 불러옴
"""
