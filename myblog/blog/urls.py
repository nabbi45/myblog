from django.urls import path
from .views import (
                        blog_post_delete_view,
                        blog_post_detail_view,
                        blog_post_list_view,
                        blog_post_update_view,
                                                )

urlpatterns = [
    path('',blog_post_list_view),
    path('<str:slug>/',blog_post_detail_view),
    path('<str:slug>/edit/',blog_post_update_view),
    path('<str:slug>/delete/',blog_post_delete_view),
    #if i do path('blog/<str:post_id>',blog_post_detail_view), it'd give error. This is server side error
    # and user don't wanna see this. So to handle these erros we use http404 exception in views.
]
