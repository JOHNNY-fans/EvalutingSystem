"""EvalutingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from comments import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^comment_list/', views.comment_list, name='comment_list'),  # 0前半个参数表示访问时的路径（用来匹配参数的正则表达式），后半个参数表示view文件里函数
    url(r'^comment/', views.comment),  # view文件里的comment函数
    url(r'^teacher_submit/', views.teacher_submit),
    url(r'^login/',views.login),
    url(r'^submit/', views.submit),  # view文件里的submit函数
    url(r'^lesson_all/', views.lesson_all),  # 前半个参数表示访问时的路径（用来匹配参数的正则表达式），后半个参数表示view文件里函数
    url(r'^teacher_by_lesson/', views.teacher_by_lesson),
    url(r'^lesson_by_teacher/', views.lesson_by_teacher),
    url(r'^back_to_index/', views.back_to_index),
    url(r'^KNN_teacher/', views.KNN_teacher),
    url(r'^logout/', views.logout),
]
