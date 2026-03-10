from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailLoginForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='pompom/login.html',
        authentication_form=EmailLoginForm
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login-redirect/', views.login_redirect_view, name='login_redirect'),
    path('dashboard/', views.landlord_dashboard_view, name='landlord_dashboard'),
    path('property/<int:property_id>/', views.property_detail_view, name='property_detail'),
    path('property/<int:property_id>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites_view, name='my_favorites'),
    path('update-info/', views.update_personal_info_view, name='update_info'),
    path('property/<int:property_id>/book/', views.create_booking_view, name='create_booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('dashboard/', views.landlord_dashboard_view, name='landlord_dashboard'),
    path('booking/<int:booking_id>/process/', views.process_booking_view, name='process_booking'),
    path('dashboard/add-property/', views.add_property_view, name='add_property'),
    path('dashboard/property/<int:property_id>/delete/', views.delete_property_view, name='delete_property'),
    path('dashboard/property/<int:property_id>/edit/', views.edit_property_view, name='edit_property'),
    path('booking/<int:booking_id>/pay/', views.create_checkout_session_view, name='pay_booking'),
]