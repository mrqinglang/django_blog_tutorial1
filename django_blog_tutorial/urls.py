"""django_blog_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# 引入views.py
from article import views
# 图片
from django.conf import settings
from django.conf.urls.static import static
app_name = 'article'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('article-list/', views.article_list, name='article_list'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:id>/', views.article_updata, name='article_update'),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),
    path('comment', include('comment.urls', namespace='comment')),
]

#添加这行
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
