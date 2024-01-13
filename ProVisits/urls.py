from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [
    ############################################################
    ######################## Users Urls ########################
    ############################################################
    path('dashboard/', views.Dashboard),
    path('analytics/', views.Analytics),
    path('membership/', views.Membership),
    path('settings/', views.Settings),
    path('closeaccount/', views.CloseAccount),
    path('changepassword/', views.ChangePassword),
    path('getmembership/<str:tp>/', views.GetMemberShip),
    path('cards/', views.Cards),
    path('products/', views.Products),
    path('product/<str:PID>/', views.Product),
    path('addproduct/', views.AddProduct),
    path('editproduct/<str:PID>/', views.EditProduct),
    path('deleteproduct/<str:PID>/', views.DeleteProduct),
    path('messages/', views.Messages),
    path('message/<str:messageID>/', views.Message),
    path('addnewcard/', views.AddNewCard),
    path('editcard/<str:cardname>/', views.EditCard),
    path('deletecard/<str:cardname>/', views.DeleteCard),

    ############################################################
    ######################## Global Urls #######################
    ############################################################
    path('', views.HomePage),
    path('about/', views.AboutPage),
    path('testimonials/', views.TestimonialsPage),
    path('contactus/', views.ContactUsPage),
    path('signin/', views.SignInPage),
    path('signup/', views.SignUpPage),
    path('logout/', views.logout),
    path('manifesto/', views.Manifesto),
    path('productt/', views.Productt),
    path('bugs/', views.Bugs),
    path('card/<str:cardname>/', views.ViewCard),
    path('sourcecode/', views.SourceCode),
    path('profile/<str:username>/', views.Profile),
    ############ Payment Handler ################
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)