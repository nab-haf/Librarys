from django.urls import path
from . import views 

urlpatterns = [
    
    # path('',views.Index,name='home'),
    
    path('',views.HomePage.as_view(),name='homepage'),
    
    path('Books',views.all,name='all'),
    
    path('contact',views.contact,name='contact'),
   
    path('About',views.aboutpageview.as_view(),name='about'),

    path('list/',views.booklistview.as_view(),name='List_Book'),
    
    path('books/add',views.BookCreateView.as_view(),name='books_add'),
    
    path('dash/',views.BookListView.as_view(),name='dash'),
    
    path('books/',views.BookListView.as_view(),name='book_list'),
    
    path('category/',views.CategoryListView.as_view(),name='list_cate'),
    
    path('author/',views.AuthorListView.as_view(),name='list_auth'),
    
    
    path('books/edit/<int:pk>',views.BookUpdateView.as_view(),name='books_edit'),

    path('books/detail/<int:pk>',views.BookDetailView.as_view(),name='books_detail'),
    
    path('books/Delete/<int:pk>',views.BookDeleteView.as_view(),name='books_delete'),

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


    path('dash/books', views.BookListView.as_view(), name='books'),
    path('dash/categories/', views.CategoryListView.as_view(), name='categories'),
    path('dash/authors/', views.AuthorListView.as_view(), name='authors'),

    path('dash/books/add/', views.BookCreateView.as_view(), name='add_book'),
    path('dash/categories/add/', views.AddCategoryViews.as_view(), name='add_category'),
    path('dash/authors/add/', views.AddAuthorViews.as_view(), name='add_author'),

    path('dash/books/<int:pk>/edit/', views.BookUpdateViews.as_view(), name='update_book'),
    path('dash/categories/<int:pk>/edit/', views.CategoryUpdateViews.as_view(), name='update_category'),
    path('dash/authors/<int:pk>/edit/', views.AuthorUpdateViews.as_view(), name='update_author'),

    path('dash/books/<int:pk>/delete/', views.BookDeleteViews.as_view(), name='delete_book'),
    path('dash/categories/<int:pk>/delete/', views.CategoryDeleteViews.as_view(), name='delete_category'),
    path('dash/authors/<int:pk>/delete/', views.AuthorDeleteViews.as_view(), name='delete_author'),

    path('dash/books/<int:pk>/', views.BookDetailViews.as_view(), name='book_detail'),
    path('dash/categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('dash/authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),


]