from django.urls import path
from wish import views



urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('wish_item/create', views.create_item),
    path('wish_item/<int:id>', views.view_item),
    path('delete/<int:id>', views.delete),
    path('add_item/<int:id>', views.add_item),
    path('cancel/<int:id>', views.cancelitem),
]