from itertools import count
from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Category,Author,Book,Borrowing,Member
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Permission,User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import loginform,loginmember,bookform ,categoryform,authorform,memberform
from django.views.generic import ListView, TemplateView,CreateView,UpdateView,DeleteView,DetailView
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import Http404
import base64
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import  assign_perm,get_objects_for_user
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# start class based view--------------------------------------------------------------------
class ListViewGeneric(ListView):

    template_name = "dash/ListView.html"
    
    model_name = None
    fields = []
    headers = []
    columns = None
    add_url = None
    update_url = None
    delete_url = None
    detail_url = None
    show_add_button=None
    permission_required=None
    all_permissions = PermissionRequiredMixin

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_add_button']=self.request.user.has_perm()
        context["model_name"] = self.model_name
        context['columns'] = self.columns
        context["fields"] = self.fields
        context["headers"] = self.headers
        context["add_url"] = self.add_url
        context['update_url'] = self.update_url 
        context['delete_url'] = self.delete_url
        context['detail_url'] = self.detail_url
        
        context["objects"] = context["object_list"]
        return context 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['show_add_button']=self.request.user.has_perm()
        context["model_name"] = self.model_name
        context['columns'] = self.columns
        context["fields"] = self.fields
        context["headers"] = self.headers
        context["add_url"] = self.add_url
        context['update_url'] = self.update_url 
        context['delete_url'] = self.delete_url
        context['detail_url'] = self.detail_url
        
        context["objects"] = context["object_list"]

        # def get_queryset(self):
        #      permission = self.get_required_permission()

        #      if self.request.user.has_perm(permission):
        #         return get_objects_for_user(
        #         self.request.user,
        #         permission,
        #         self.model
        #         )

        # context['user_permissions_list']=self.request.user.get_all_permissions()
        # permission for all model
        
        try:
             context["can_view"] = self.request.user.has_perm(
                            f"{self.model._meta.app_label}.view_{self.model._meta.model_name}"
                             )
             context["can_add"] = self.request.user.has_perm(
                                f"{self.model._meta.app_label}.add_{self.model._meta.model_name}"
                                )
             context["can_change"] = self.request.user.has_perm(
                                f"{self.model._meta.app_label}.change_{self.model._meta.model_name}"
                                )
             context["can_delete"] = self.request.user.has_perm(
                                f"{self.model._meta.app_label}.delete_{self.model._meta.model_name}"
                             )
        except User.DoesNotExist:
        
            context["error"]="Error"
        return context 


class BaseFormView:

    list_url_name=None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        context['list_url'] = self.list_url_name
        return context


class BookListView(ListViewGeneric):
    model=Book
    model_name = "Book"
    # columns=['title','author','categ']
    columns = ["image","title", "author","categ"]
    headers = [" Book ","Title", "Author","Category"]
    add_url = reverse_lazy("books_add")
    update_url = ("update_book")
    delete_url = ("delete_book")
    detail_url = ("book_detail") 
    
    print(PermissionRequiredMixin)
    Permission_required='main.view_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['show_add_button']=self.request.user.has_perm("main.view_category")
        context['user_permissions_list']=self.request.user.get_all_permissions()
        return context 
    
    # def get_queryset(self):
    #     return get_objects_for_user(
    #     self.request.user,
    #     self.request.user.get_all_permissions(),
    #     Book
    #     )
    

class UserListView(ListViewGeneric):
    model=User
    model_name = "User"
    columns = ["username","password"]
    headers = [" Name ","Password"]
    add_url = reverse_lazy("add_user") 
    update_url = ("update_user")
    delete_url = ("delete_user")
    detail_url = ("user_detail")

class AddUserViews(BaseFormView,CreateView):
    model=User
    model_name = "User"
    list_url_name = 'users' 
    fields=['username','password']
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("users")

def AddUser(request):
    
   if (request.POST) :
    
    add_form=UserCreationForm(request.POST,request.FILES)
      
    if(add_form.is_valid()):
        
        add_form.save()
        return redirect('dash')

   else :
       add_form=UserCreationForm()

   return render(request,'dash/user_form.html',{'form':add_form})


class CategoryListView(ListViewGeneric):
    model=Category
    model_name = "Category"
    columns = ["name"]
    headers = ["Category Name "]
    add_url = reverse_lazy("add_categories") 
    update_url = ("update_category")
    delete_url = ("delete_category")
    detail_url = ("category_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['show_add_button']=self.request.user.has_perm("main.view_category")
        context['user_permissions_list']=self.request.user.get_all_permissions()
        return context 

class AuthorListView(ListViewGeneric):
    model=Author
    model_name = "Author"
   
    columns = ['author','about']
    headers = ['Author Name','About']
    add_url = reverse_lazy("add_author") 
    update_url = ("update_author")
    delete_url = ("delete_author")
    detail_url = ("author_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['show_add_button']=self.request.user.has_perm("main.view_category")
        context['user_permissions_list']=self.request.user.get_all_permissions()
        return context 



class AddBookViews(BaseFormView,PermissionRequiredMixin,CreateView):
    model=Book
    list_url_name = 'books' 
    fields=['title','date_pub','publisher','description','image','categ','author','page_num','file']
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("books")

    Permission_required="main.view_book"

    def form_valid(self,form):
        response=super().form_valid(form)
        assign_perm('view_book', self.request.user,self.object)
        assign_perm('change_book', self.request.user,self.object)
        assign_perm('delete_book', self.request.user,self.object)
        return  response

    
class BookUpdateViews(BaseFormView,UpdateView):
   model=Book
   list_url_name = 'books' 
   fields=['title','date_pub','publisher','description','image','categ','author','page_num','file']
   template_name='dash/base_form.html'
   success_url = reverse_lazy("books")

class BookDeleteViews(BaseFormView,DeleteView):
   model=Book
   list_url_name = 'books' 
   template_name='dash/conf_delete.html'
   success_url = reverse_lazy("books")

#    categories
class AddCategoryViews(BaseFormView,CreateView):
    model=Category
    list_url_name = 'categories' 
    fields=['name']
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("categories'")
    
class CategoryUpdateViews(BaseFormView,UpdateView):
   model=Category
   list_url_name="categories"
   fields=['name']
   template_name='dash/base_form.html'
   success_url = reverse_lazy("categories")
   

class CategoryDeleteViews(BaseFormView,DeleteView):
   model=Category
   list_url_name = "categories"
   template_name='dash/conf_delete.html'
   success_url = reverse_lazy("categories")

#    Authors
class AddAuthorViews(BaseFormView,CreateView):
    model=Author
    model_name = "Author"
    list_url_name = 'authors' 
    fields=['author','about']
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("authors")
    
class AuthorUpdateViews(BaseFormView,UpdateView):
   model=Author
   list_url_name = 'authors' 
#    model_name = "Author"
   fields=['author','about']
   template_name='dash/base_form.html'
   success_url = reverse_lazy("authors")

   

class AuthorDeleteViews(BaseFormView,DeleteView):
   model=Author
   model_name = "Author"
   list_url_name = 'authors' 
   template_name='dash/conf_delete.html'
   success_url = reverse_lazy("authors")

class DetailViewGeneric (DetailView):
    model = None
    template_name = "dash/Detailobj.html"
    context_object_name = "object"
    list_url = None
    update_url = None
    delete_url = None
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        context['list_url'] = self.list_url
        context['update_url'] = self.update_url
        context['delete_url'] = self.delete_url
        context['model_name'] = self.model._meta.verbose_name.title()
        context['fields'] = [field for field in self.object._meta.get_fields() if field.concrete]
        fields_info = []
        for field in self.object._meta.get_fields():
            if not getattr(field, 'concrete', False):
                continue
            value = getattr(self.object, field.name)
            fields_info.append({
                'label': field.verbose_name,
                'value': value,
                'is_image': field.__class__.__name__ == "ImageField",
                'is_many_to_many': field.__class__.__name__ == "ManyToManyField",
            })
        context['fields_info'] = fields_info

        return context

class BookDetailViews(DetailViewGeneric):
    model = Book
    template_name = "dash/Detailobj.html"
    context_object_name = "book"
    list_url = "books"
    update_url = "update_book"
    delete_url = "delete_book"



class CategoryDetailView(DetailViewGeneric):
    model = Category
    template_name = "dash/Detailobj.html"
    context_object_name = "category"
    list_url = "categories"
    update_url = "update_category"
    delete_url = "delete_category"

class AuthorDetailView(DetailViewGeneric):
    model = Author
    template_name = "dash/Detailobj.html"
    context_object_name = "author"
    list_url = "authors"
    update_url = "update_author"
    delete_url = "delete_author"

# end class based view--------------------------------------------------------------
    
def Index(request):
    categ=Category.objects.all()
    book=Book.objects.all()
    return render(request,'main/index.html',{'categorys':categ ,'Books':book})

def Category_Books(request,cate):
   
   
   categ1=Book.objects.filter(categ__name=cate)
   return render(request,'main/book_card.html',{'Books':categ1})


class HomePage(TemplateView):
   template_name='main/index.html'
   def get_context_data(self,**kwargs):
      context=super().get_context_data(**kwargs)
      context['Books']=Book.objects.all()

      cat_id =self.request.GET.get('cat')

      if cat_id:
            context['books_by_category'] =  Book.objects.filter(categ__id=cat_id)
      else:
          context['books_by_category'] =  Book.objects.all()

      context['Books_new']=Book.objects.order_by('date_pub')[:3]
      context['category']=Category.objects.all()
      context['Book_cu']=context['Books_new'].annotate(num_book=Count('title'))
      

      return context
   


def contact(request):
   
    return render(request,'main/Contact.html')


class booklistview(ListView):
   model=Book
   template_name='dashboard/Book_list.html'
   context_object_name='Books'
   ordering=['title']
   paginate_by=3
   

class aboutpageview(TemplateView):
   template_name='main/about.html'


class BookCreateView(CreateView):
   model=Book
   fields=['title','date_pub','publisher','description','image','categ','author','page_num','file']
   template_name='dashboard/Book_add.html'
   success_url=reverse_lazy('List_Book')

class BookUpdateView(UpdateView):
   model=Book
   fields=['title','date_pub','publisher','description','image','categ','author','page_num','file']
   template_name='dashboard/Book_detail.html'
   success_url=reverse_lazy('List_Book')

class BookDeleteView(DeleteView):
   model=Book
   template_name='dashboard/Book_delete.html'
   success_url=reverse_lazy('List_Book')


class BookDetailView(DetailView):
   model=Book
   template_name='main/Book_single.html'
   


def all(request):
    
    categ=Category.objects.all()
    book=Book.objects.all()
    borrow=Borrowing.objects.all()
    author=Author.objects.all()

    # Book status

    borrowed_books = Borrowing.objects.filter(is_returned=False).values_list('book__title', flat=True)


    Categ_id=request.GET.get('category')

    if Categ_id and Categ_id != "" :
        book=book.filter(categ=Categ_id)


    author_id=request.GET.get('author')
    
    if author_id and author_id != "" :
        book=book.filter(author=author_id)
   

    paginator = Paginator(book,2)  # Show 2 Book per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
   
    return render(request,'main/all_books.html',
                  {
                   'page_obj':page_obj ,
                   'categorys':categ ,
                   'Books':book,
                   'Borrow':borrow,
                   'authors':author,
                   'borrowed_books': borrowed_books })


def login_view(request):
    login_form=loginform()
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
           
            return redirect("dash")
        else:
            return render(request,'main/login.html',{'error':"Invalid credentials",'form':login_form})
        
    return render(request,"main/login.html",{'form':login_form})    


def logout_view(request):
    logout(request)
    return redirect("admin-site")

def single_book(request,id):
   Books1=get_object_or_404(Book,pk=id)
   return render(request,'main/Book_single.html',{'Book':Books1})


def dashboard(request):
    categ=Category.objects.all()
    book=Book.objects.all()
    
    author=Author.objects.all()
    member=Member.objects.all()

    categories = Category.objects.annotate(book_count=Count('books'))

    return render(request,'dashboard/index.html',{
        'categorys':categ ,
        'Books':book,
        'count':categories
        ,'author':author,
        'member':member})


def category_detail(request,cate):
    category = get_object_or_404(Category,name=cate)
    books = category.books.all() # Access related Book using related_name
    
    context = {
        'category': category,
        'books': books,
    }
    return render(request, 'dashboard/index.html', context)


def login_member(request,id):

    login_for=loginmember()
   

    if request.method=="POST":
        name1=request.POST.get("membername")
        password=request.POST.get("password")
        memb=Member.objects.all()
        for member in memb :       
           if  member.name==str(name1) and member.password==str(password) :
               Books1=get_object_or_404(Book, pk=id)
               memb1=get_object_or_404(Member,name=name1)
               return render(request,'main/Book_member.html',{'Book':Books1,'member':memb1})

    
           
        return render(request,'main/loginmember.html',{'error':"Invalid credentials",'form':login_for})
        
    return render(request,"main/loginmember.html",{'form':login_for})    

def login_memberf(request):

    login_for=loginmember()
   

    if request.method=="POST":
        name1=request.POST.get("membername")
        password=request.POST.get("password")
        memb=Member.objects.all()
        for member in memb :  
             
           if  member.name==str(name1) and member.password==str(password) :
               Books1=Book.objects.all()
               borrow=Borrowing.objects.all()
               memb1=get_object_or_404(Member,name=name1)

               borrow_r = Borrowing.objects.filter(member_id=memb1.id)

               return render(request,'main/profilemember.html',{'Book':Books1,'member':memb1,'Borrow':borrow ,'borrow_r':borrow_r})

            
           
        return render(request,'main/loginmember.html',{'error':"Inalid credentials",'form':login_for})
        
    return render(request,"main/loginmember.html",{'form':login_for})    


def pdf_page(request,id):

    try:
     pdf = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        raise Http404("File does not exist")

    pdf_path = pdf.file.path
    with open(pdf_path, 'rb') as pdf_file:
        # Convert pdf to a string
        pdf_content = base64.b64encode(pdf_file.read()).decode()

    context = {
        "pdf": pdf_content,
    }

    return render(request, "main/pdf_page.html", context)


def profile_memb(request,name):

    member = get_object_or_404(Member, name=name)

    borrow_r = Borrowing.objects.filter(member_id=name)

    

    return render(request,'main\profilemember.html',{'member':member})




 
def Register(request):
    
   if (request.POST) :
    
    add_form=memberform(request.POST,request.FILES)
      
    if(add_form.is_valid()):
        name=request.POST.get("name")
        add_form.save()
        return redirect('profile',name=name)

   else :
       add_form=memberform()

   return render(request,'main/add_member.html',{'form':add_form})


@login_required(login_url='/login/')
def book_add(request):
    
   if (request.POST) :
    add_form=bookform(request.POST,request.FILES)  
    if(add_form.is_valid()):
        add_form.save()
        return redirect('dashboard')

   else :
       add_form=bookform()

   return render(request,'dashboard/Book_add.html',{'form':add_form})



@login_required(login_url='/login/')
def categ_add(request):
    
   if (request.POST) :
    categ_form=categoryform(request.POST,request.FILES)  
    if(categ_form.is_valid()):
        categ_form.save()
        return redirect('dashboard')

   else :
       categ_form=categoryform()
    #    print(categ_form.errors.as_data()) # here you print errors to terminal

   return render(request,'dashboard/add_category.html',{'formc':categ_form})


@login_required(login_url='/login/')
def author_add(request):
    

   if (request.POST) :
    add_form=authorform(request.POST,request.FILES)  
    if(add_form.is_valid()):
        add_form.save()
        return redirect('dashboard')

   else :
       add_form=authorform()

   return render(request,'dashboard/Author_add.html',{'forma':add_form})


# @login_required
# def member_profile(request):

#     Borrow_book=Borrowing.objects.filter(member__user=request.user, is_returned=False).count()
   
#     cost_m=Borrowing.objects.filter(member__user=request.user, cost_c=0).aggregate(count('cost')) ['cost_count'] or 0

#     return render(request, "main/member_profile.html",)

