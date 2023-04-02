from django.urls import path
from . import views


urlpatterns = [
 path('', views.home,name="home" ),
 path('commerce', views.commerce,name="commerce" ),
 path('faculty', views.faculty,name="faculty" ),
 path('contactus', views.contactus,name="contactus" ),
 path('profile', views.profile,name="profile" ),
 path('documents', views.documents,name="documents" ),
 path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
 path('dashboard', views.dashboard,name="dashboard" ),
 path("password_reset", views.password_reset_request, name="password_reset"),
 path('register', views.register_request, name="register"),
 path('login', views.login_request, name="login"),
 path("logout", views.logout_request, name= "logout"),
]