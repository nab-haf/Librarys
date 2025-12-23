from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    

    def __str__(self):
        return str(self.name)

class Author(models.Model):
    author=models.CharField(max_length=100)
    about=models.CharField(max_length=100)
  
    def __str__(self):
        return str(self.author)

class Book(models.Model):
    title=models.CharField(max_length=100)
    date_pub=models.DateField(null=True)
    publisher=models.CharField(max_length=20)
    # copies=models.CharField()
    description=models.TextField(null=True)
    image=models.ImageField(upload_to='photos')
    categ=models.ManyToManyField('Category', related_name='books')
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    page_num=models.IntegerField()
    file = models.FileField(upload_to='files',null=True)
   
    class  Mate:

        permissions = [
        ('can_publish', 'Can publish '),
        ('can_edit_published', 'Can edit published '),
    ]    
        
    def __str__(self):
        return str(self.title)

  
# class Bookcop(models.Model):
#     un_id=models.IntegerField(unique=True)
#     book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
#     is_av=models.BooleanField(default=True)


#     def __str__(self):
#         return str(self.un_id)

class Member(models.Model):
    name=models.CharField(max_length=100)
    about=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=10,null=True)
    image=models.ImageField(upload_to='photos/member', null=True)
    # user=models.OneToOneField('auth.User',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.name)
    
class Borrowing(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Member,on_delete=models.CASCADE)
    borrow_date=models.DateTimeField(auto_now_add=True)
    return_date=models.DateTimeField(null=True,blank=True)
    activate_date=models.DateTimeField(null=True,blank=True)
    is_returned=models.BooleanField(default=False)
    Cost=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return str(self.book)
    


