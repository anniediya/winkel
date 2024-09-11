from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginfn),
    path('reg/', views.registerfn),
    path('samp/', views.sampfn),
    path('samp2/', views.samp2fn),
    path('home/', views.homefn, name='home'),  # This is the homepage after login
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('full/', views.full),
    path('',views.registerfn),
    path('add/',views.add_productfn),
    path('viewproduct/<int:p_id>',views.viewproductfn),
    path('about/',views.aboutfn),
    path('staff/',views.staffn),
    # path('add_categories/',views.add_categoriesfn),
    path('editproduct/<int:p_id>',views.edit_productfn),    
    path('full/', views.full),

    path('logout/', views.logout),
    path('login/', views.loginfn),
    path('reg/', views.registerfn),
    path('home/', views.homefn, name='home'),  # This is the homepage after login
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),

    

]