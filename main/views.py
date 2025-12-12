from itertools import count
from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Category,Author,Book,Borrowing,Member
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import loginform,loginmember,bookform ,categoryform,authorform,memberform
from django.views.generic import ListView, TemplateView
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import Http404
import base64

# Create your views here.

def Index(requset):
    categ=Category.objects.all()
    book=Book.objects.all()
    return render(requset,'main/index.html',{'categorys':categ ,'Books':book})

def Category_Books(request,cate):
   
   
   categ1=Book.objects.filter(categ__name=cate)
   return render(request,'main/book_card.html',{'Books':categ1})


class HomePage(TemplateView):
   template_name='main/index.html'
   def get_context_data(self,**kwargs):
      context=super().get_context_data(**kwargs)
      context['Books']=Book.objects.all()
      context['Books_new']=Book.objects.order_by('date_pub')[:3]
      context['category']=Category.objects.all()
      context['Book_cu']=context['Books_new'].annotate(num_book=Count('title'))
      

      return context
   


def contact(requset):
   
    return render(requset,'main/Contact.html')


class booklistview(ListView):
   model=Book
   template_name='dashboard/Book_list.html'
   context_object_name='Books'
   ordering=['title']

   paginate_by=3


class aboutpageview(TemplateView):
   template_name='main/about.html'




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


def login_view(requset):
    login_form=loginform()
    if requset.method=="POST":
        username=requset.POST.get("username")
        password=requset.POST.get("password")

        user=authenticate(requset,username=username,password=password)

        if user is not None:
            login(requset,user)
           
            return redirect("dashboard")
        else:
            return render(requset,'main/login.html',{'error':"Inalid credentials",'form':login_form})
        
    return render(requset,"main/login.html",{'form':login_form})    


def logout_view(requset):
    logout(requset)
    return redirect("/")

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


def login_member(requset,id):

    login_for=loginmember()
   

    if requset.method=="POST":
        name1=requset.POST.get("membername")
        password=requset.POST.get("password")
        memb=Member.objects.all()
        for member in memb :       
           if  member.name==str(name1) and member.password==str(password) :
               Books1=get_object_or_404(Book, pk=id)
               memb1=get_object_or_404(Member,name=name1)
               return render(requset,'main/Book_member.html',{'Book':Books1,'member':memb1})

    
           
        return render(requset,'main/loginmember.html',{'error':"Inalid credentials",'form':login_for})
        
    return render(requset,"main/loginmember.html",{'form':login_for})    

def login_memberf(requset):

    login_for=loginmember()
   

    if requset.method=="POST":
        name1=requset.POST.get("membername")
        password=requset.POST.get("password")
        memb=Member.objects.all()
        for member in memb :  
             
           if  member.name==str(name1) and member.password==str(password) :
               Books1=Book.objects.all()
               borrow=Borrowing.objects.all()
               memb1=get_object_or_404(Member,name=name1)

               borrow_r = Borrowing.objects.filter(member_id=memb1.id)

               return render(requset,'main/profilemember.html',{'Book':Books1,'member':memb1,'Borrow':borrow ,'borrow_r':borrow_r})

            
           
        return render(requset,'main/loginmember.html',{'error':"Inalid credentials",'form':login_for})
        
    return render(requset,"main/loginmember.html",{'form':login_for})    


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




 
def Register(requset):
    
   if (requset.POST) :
    
    add_form=memberform(requset.POST,requset.FILES)
      
    if(add_form.is_valid()):
        name=requset.POST.get("name")
        add_form.save()
        return redirect('profile',name=name)

   else :
       add_form=memberform()

   return render(requset,'main/add_member.html',{'form':add_form})


@login_required(login_url='/login/')
def book_add(requset):
    
   if (requset.POST) :
    add_form=bookform(requset.POST,requset.FILES)  
    if(add_form.is_valid()):
        add_form.save()
        return redirect('dashboard')

   else :
       add_form=bookform()

   return render(requset,'dashboard/Book_add.html',{'form':add_form})



@login_required(login_url='/login/')
def categ_add(requset):
    
   if (requset.POST) :
    categ_form=categoryform(requset.POST,requset.FILES)  
    if(categ_form.is_valid()):
        categ_form.save()
        return redirect('dashboard')

   else :
       categ_form=categoryform()
    #    print(categ_form.errors.as_data()) # here you print errors to terminal

   return render(requset,'dashboard/add_category.html',{'formc':categ_form})


@login_required(login_url='/login/')
def author_add(requset):
    

   if (requset.POST) :
    add_form=authorform(requset.POST,requset.FILES)  
    if(add_form.is_valid()):
        add_form.save()
        return redirect('dashboard')

   else :
       add_form=authorform()

   return render(requset,'dashboard/Author_add.html',{'forma':add_form})


# @login_required
# def member_profile(request):

#     Borrow_book=Borrowing.objects.filter(member__user=request.user, is_returned=False).count()
   
#     cost_m=Borrowing.objects.filter(member__user=request.user, cost_c=0).aggregate(count('cost')) ['cost_count'] or 0

#     return render(request, "main/member_profile.html",)

