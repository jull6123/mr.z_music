"""
URL configuration for newdemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from demoone.views import hviews, music, user

from django.urls import path

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('login/', hviews.login),
    path('register/', hviews.register),
    path("person/", hviews.person),
    path("update/", hviews.update),


    path("home/", hviews.home),

    # 管理员界面对用户的增删改查
    path("user/<int:uid>/search/", user.search),
    path("user/list/", user.userList),
    path("user/add/", user.userAdd),
    path("user/delete/", user.userDelete),
    path("user/<int:nid>/edit/", user.userEdit),


    path("music/down/", music.down),
    path("music/change/", music.change),
    path("music/theList/", music.theList),

    path("music/<int:uid>/search/", music.search),
    path("music/list/", music.musicList),
    path("music/add/", music.musicAdd),
    path("music/delete/", music.musicDelete),
    path("music/<int:nid>/edit/", music.musicEdit),
]

from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
