from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-booking/', views.create_booking_view, name='create_booking'),
    path('submit-review/<int:booking_id>/', views.submit_review_view, name='submit_review'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]