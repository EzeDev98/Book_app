from django.contrib import messages, auth
from django.conf import settings
import re
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Story

# Create your views here.


@login_required(login_url = 'login')
def home(request):
    books = Story.objects.order_by('created_date')
    data = {
        'books': books,
    }
    return render(request, 'book/home.html', data)


def about(request):
    return render(request, 'book/about.html')


def landing_page(request):
    return render(request, 'book/landing-page.html')


@login_required(login_url = 'login')
def service(request):
    return render(request, 'book/home.html')


def story_page(request, id):
    tale = get_object_or_404(Story, pk=id)
    
    words_per_page = 4000
    words = tale.story_body.split()  # Splitting into words
    
    paginated_content = []
    current_page = []
    current_word_count = 0
    
    for word in words:
        if current_word_count + len(word) <= words_per_page:
            current_page.append(word)
            current_word_count += len(word) + 1  # +1 for space
        else:
            paginated_content.append(" ".join(current_page))
            current_page = [word]
            current_word_count = len(word) + 1
    
    if current_page:
        paginated_content.append(" ".join(current_page))
    
    page = request.GET.get('page')
    paginator = Paginator(paginated_content, 1)
    
    try:
        paged_story = paginator.page(page)
    except PageNotAnInteger:
        paged_story = paginator.page(1)
    except EmptyPage:
        paged_story = paginator.page(paginator.num_pages)
    
    data = {
        "tale": tale,         # Pass the entire tale
        "paged_story": paged_story,  # Pass the paginated content
    }
    return render(request, 'book/story_page.html', data)



@login_required(login_url = 'login')
def search(request):
    search_results = Story.objects.order_by('-created_date')
    
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            search_results = search_results.filter(book_title__icontains=search)
            
    data = {
        'search_results': search_results,
    }
        
    return render(request, 'book/search.html', data)


def search_page(request, id):
    search = get_object_or_404(Story, pk=id)
    
    words_per_page = 4000
    words = search.story_body.split()
    
    paginated_content = []
    current_page = []
    current_word_count = 0
    
    for word in words:
        if current_word_count + len(word) <= words_per_page:
            current_page.append(word)
            current_word_count += len(word) + 1
        else:
            paginated_content.append(" ".join(current_page))
            current_page = [word]
            current_word_count = len(word) + 1
            
    if current_page:
        paginated_content.append(" ".join(current_page))
        
    page = request.GET.get('page')
    paginator = Paginator(paginated_content, 1)
    
    try:
        paged_story = paginator.page(page)
    except PageNotAnInteger:
        paged_story = paginator.page(1)
    except:
        paged_story = paginator.page(paginator.num_pages)
        
    data = {
        'search': search,
        'paged_story': paged_story,
    }
    return render(request, 'book/search_page.html', data)


@login_required(login_url = 'login')
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        subject = subject
        message = "You have a new message from " + name + ". " + "The subject of the message is: " + subject + ". " + "This is the message: " + message
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['ezemosesjohn21997@gmail.com'],
            fail_silently=False
        )
        success  = "Hello!, We've received your message. We would get back to you shortly!"
        return render(request, 'book/contact.html', {'success': success})
    return render(request, 'book/contact.html')



def form(request):
    if request.method == 'POST':
        booktitle = request.POST['booktitle']
        storytitle = request.POST['storytitle']
        chapter = request.POST['chapter']
        author = request.POST['author']
        edition = request.POST['edition']
        language = request.POST['language']
        origin = request.POST['origin']
        story = request.POST['story']
        Story.objects.create(book_title=booktitle, story_title=storytitle, chapter=chapter, author=author, edition=edition, language=language, origin=origin, story_body=story)
        return redirect('/')   
    return render(request, 'book/form.html')




def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            
            if User.objects.filter(username=username).exists():
                error = 'Username already exists, kindly enter a different username!'
                return render(request, 'book/signup.html', {'error': error})
            else: 
                if User.objects.filter(email=email).exists():
                    error = 'Email already exists, kindly enter a different email address!'
                    return render(request, 'book/signup.html', {'error': error})
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, password=password, email=email, username=username)
                    user.save()
                    return redirect('login')
            
        else:
            error = 'Passwords do not match, kindly enter a correct password!'
            return render(request, 'book/signup.html', {'error': error})
               
    else:
        return render(request, 'book/signup.html')
    
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, user)
            return redirect('landing_page')
        else:
            error = 'Invalid credentials. Login with correct details!'
            return render(request, 'book/login.html', {'error': error})
    else:     
        return render(request, 'book/login.html')
    
    
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')
    return redirect('home')


@login_required(login_url = 'login')
def premium(request):
    return render(request, 'book/home')


@login_required(login_url = 'login')
def projects(request):
    return render(request, 'book/home')


@login_required(login_url = 'login')
def sponsors(request):
    return render(request, 'book/home')


@login_required(login_url = 'login')
def mentorship(request):
    return render(request, 'book/home')


@login_required(login_url = 'login')
def portfolio(request):
    return render(request, 'book/home')