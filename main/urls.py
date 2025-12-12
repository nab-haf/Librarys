from django.urls import path
from . import views 

urlpatterns = [
    
    # path('',views.Index,name='home'),
    
    path('',views.HomePage.as_view(),name='homepage'),
    
    path('Books',views.all,name='all'),
    
    path('contact',views.contact,name='contact'),
   
    path('About',views.aboutpageview.as_view(),name='about'),

    path('list/',views.booklistview.as_view(),name='List_Book'),

    path('login/',views.login_view,name='login'),
    
    path('loginmember/<int:id>',views.login_member,name='loginmem'),

    path('member',views.login_memberf,name='pro_memb'),
    
    path('admin-site/',views.login_view,name='admin-site'),
   
    path('logout/',views.logout_view,name='logout'),

    path('Book/<int:id>',views.single_book,name='single_book'),

    path('dashboard',views.dashboard,name='dashboard'),

    path('pdf_page/<int:id>', views.pdf_page, name='pdf_page'),

    path('add/',views.book_add,name='add_Book'),

    path('register/',views.Register,name='Register'),

    path('categ_add',views.categ_add,name='add_categ'),

    path('author_add',views.author_add,name='add_auth'),
    
    path('profile/<str:name>',views.profile_memb,name='profile'),

    path("Category/<str:cate>",views.Category_Books,name='one_category'),

    path('category/<str:cate>/', views.category_detail, name='category_detail'),

]