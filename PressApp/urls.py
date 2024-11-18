from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('news-page/<int:pk>/', views.news_page, name='news_page'),
    path('news-by-date/<str:foo>/', views.news_by_date, name='news_by_date'),
    path('news-by-category/<str:foo>/', views.news_by_category, name='news_by_category'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_user, name='register'),
    path('allnews/', views.allnews, name='allnews'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-article/<int:pk>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:pk>/', views.delete_article, name='delete_article'),
    path('categories/', views.categories, name='categories'),
    path('allcatnews/<str:foo>/', views.allcatnews, name='allcatnews'),
    path('delete-com/<int:pk>/', views.delete_com, name='delete_com'),
    path('add-category/', views.add_category, name='add_category'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('messages/', views.message, name='messages'),
    path('message-page/<int:pk>/', views.message_page, name='message_page'),
    path('delete-contact/<int:pk>/', views.delete_contact, name='delete_contact'),
]

handler404 = views.custom_404_view