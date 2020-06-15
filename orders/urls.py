from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registration", views.register, name="registration"),
    path("login", views.login_u, name="login"),
    path("logout", views.logout_u, name="logout"),
    path("menu/<str:category>", views.menu, name="menu"),
    path("add/<str:category>/<str:name>/<str:price>", views.add, name="add"),
    path("delete/<str:category>/<str:name>/<str:price>", views.delete, name="delete"),
    path("user_orders/<str:order_number>", views.user_orders, name="user_orders"),
    path("confirmed/<str:order_number>", views.confirmed, name="confirmed"),
    path("admin_orders/<str:user>/<str:order_number>", views.admin_orders, name="admin_orders"),
    path("complete_order/<str:user>/<str:order_number>", views.complete_order, name="complete_order"),
]