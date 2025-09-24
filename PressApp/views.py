from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import *
from django.db.models import Q
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, user_logged_in, authenticate
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Create your views here.
def main (request):

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A") 
    today_news = Article.objects.filter(Q(add_date__gte=today) & Q(edit_date__gte=today)).order_by('-add_date')
    week_ago = today - datetime.timedelta(days=7)
    week_news = Article.objects.filter(Q(add_date__gte=week_ago) & Q(edit_date__gte=week_ago)).exclude(id__in=today_news).order_by('-add_date')
    mounth_ago = today - datetime.timedelta(days=30)
    mounth_news = Article.objects.filter(Q(add_date__gte=mounth_ago) & Q(edit_date__gte=mounth_ago)).exclude(id__in=week_news).exclude(id__in=today_news).order_by('-add_date')

    last_news = Article.objects.filter(Q(add_date__gte=mounth_ago) & Q(edit_date__gte=mounth_ago)).order_by('-add_date')

    special_news = Article.objects.filter(is_special=True).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date')

    categories = Category.objects.all()

    advertisment = Advertisment.objects.all()
    allnews = Article.objects.all().order_by('-add_date')

    if 'search-bar' in request.GET:
        searched = request.GET['search-bar']
        if searched:
            # Filter products based on the search query
            allnews = allnews.filter(Q(title__icontains=searched) | Q(info__icontains=searched) | Q(content__icontains=searched)| Q(category__name__icontains=searched)| Q(add_date__icontains=searched)| Q(journalist__author__user__first_name__icontains=searched))
            if not allnews:
                err = f'No results for {searched} \n Try checking your spelling or use more general terms'


    context = {
        'today':today,
        'today_str':today_str,
        'today_news':today_news,
        'week_news':week_news if week_news else allnews,
        'mounth_news':mounth_news if mounth_news else allnews,
        'last_news':last_news if last_news else allnews,
        'special_news':special_news,
        'categories':categories,
        'trending_news':trending_news,
        'advertisment':advertisment,
        'allnews':allnews,
            }

    return render(request, 'index.html', context)

def allnews(request):

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    allnews = Article.objects.all().order_by('-add_date')
    special_news = Article.objects.filter(is_special=True).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date')

    categories = Category.objects.all()
    advertisment = Advertisment.objects.all()

    err = None
    if 'search-bar' in request.GET:
        searched = request.GET['search-bar']
        if searched:
            # Filter products based on the search query
            allnews = allnews.filter(
                Q(title__icontains=searched) |
                Q(info__icontains=searched) |
                Q(content__icontains=searched) |
                Q(category__name__icontains=searched) |
                Q(add_date__icontains=searched) |
                Q(journalist__author__first_name__icontains=searched)|
                Q(journalist__author__last_name__icontains=searched)
            )
            if not allnews:
                err = f'No results for {searched} \n Try checking your spelling or use more general terms'

    context = {
        'today':today,
        'today_str':today_str,
        'articles':allnews,
        'special_news':special_news,
        'categories':categories,
        'trending_news':trending_news,
        'advertisment':advertisment,
        'err':err,
    }
    return render(request, 'allnews.html', context)


def news_page(request, pk):

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")

    # use try , except with object.get
    try :
        article = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        messages.error(request, "This article not Available")
        return redirect('home')

    if request.user.is_authenticated:
        # التحقق إذا كان المستخدم قد شاهد المقال من قبل
        if not article.viewed_by.filter(id=request.user.id).exists():
            # إذا لم يشاهد المقال من قبل، أضف المستخدم وزد العدد
            article.viewed_by.add(request.user)
            article.num_of_views += 1
            article.save(update_fields=['num_of_views'])

    special_news = Article.objects.filter(is_special=True).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date')

    categories = Category.objects.all()
    advertisment = Advertisment.objects.all()

    try:
        article = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        messages.error(request, "This article not Available")
        return redirect('home')



    comments = Comment.objects.filter(article=article)
    num_of_comments = comments.count()

    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST':

            name = f'{request.user.first_name} {request.user.last_name}'
            email = request.user.email
            comment_text = request.POST.get('comment')

            if name and email and comment_text:
                comment = Comment.objects.create(
                    name=f'{request.user.first_name} {request.user.last_name}',  # استخدام اسم المستخدم تلقائيًا
                    email=request.user.email,    # استخدام البريد الإلكتروني تلقائيًا
                    comment=comment_text,
                    article=article,
                    creator=request.user  # ربط التعليق بالمستخدم

                )
                messages.success(request, "تم رفع تعليقك بنجاح.")
                # هنا نستخدم redirect لمنع إعادة إرسال البيانات عند إعادة تحميل الصفحة
                return redirect('news_page', pk=article.pk)
            else:
                messages.error(request, "يرجى ملئ الحقول.")
    else:
        messages.error(request, "رجاء تسجيل الدخول اولاً.")
        redirect('news_page', pk=article.pk)

    context = {
        'today_str': today_str,
        'article':article,
        'special_news':special_news,
        'trending_news':trending_news,
        'categories':categories,
        'today':today,
        'advertisment':advertisment,
        'comments':comments,
        'num_of_comments':num_of_comments,
    }

    return render(request, 'news_page.html', context)


def news_by_date(request, foo):

    foo = parse_datetime(foo)

    
    news = Article.objects.filter(add_date__date=foo.date()).order_by('-add_date')
    special_news = Article.objects.filter(Q(add_date__date=foo.date()) & Q(is_special=True)).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date').order_by('-add_date')
    categories = Category.objects.all()

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    advertisment = Advertisment.objects.all()

    context = {
        'foo':foo,
        'today_str': today_str,
        'news':news,
        'special_news':special_news,
        'trending_news':trending_news,
        'categories':categories,
        'today':today,
        'advertisment':advertisment,
    }
    return render(request, 'date_news.html', context)




def news_by_category(request, foo):

    foo = foo.replace('-', ' ')

    
    news = Article.objects.filter(category__name=foo).order_by('-add_date')
    special_news = Article.objects.filter(Q(category__name=foo) & Q(is_special=True)).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date').order_by('-add_date')
    categories = Category.objects.all()

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    advertisment = Advertisment.objects.all()

    context = {
        'foo':foo,
        'today_str': today_str,
        'news':news,
        'special_news':special_news,
        'trending_news':trending_news,
        'categories':categories,
        'today':today,
        'advertisment':advertisment,
    }
    return render(request, 'category_news.html', context)


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 :
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                user.save()
                login(request, user)
                messages.success(request, 'تم انشاء الحساب بنجاح.')
                return redirect('home')
    else:
        return render(request, 'register.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=username, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح .")
            return redirect('home')
        else:
            messages.error(request, "عذرا الإيميل او كلمة المرور غير صحيحة.")
            return redirect('login')
    else:
        return render(request, 'parts/login.html')

def user_logout(request):

    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح .")
    return redirect('home')



def dashboard(request):
    if request.user.is_staff and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        advertisment = Advertisment.objects.all()
        articles = Article.objects.filter(journalist__author__id=request.user.id).order_by('-add_date')
        categories = Category.objects.all()
        err = None

        if 'search-bar' in request.GET:
            searched = request.GET['search-bar']
            if searched:
                articles = articles.filter(
                    Q(title__icontains=searched) |
                    Q(info__icontains=searched) |
                    Q(content__icontains=searched) |
                    Q(category__name__icontains=searched) |
                    Q(add_date__icontains=searched) 
                )
                if not articles:
                    err = f'No results for {searched} \n Try checking your spelling or use more general terms'

        # إضافة مقال
        if request.method == 'POST' and 'article_id' not in request.POST:
            title = request.POST['title']
            category_id = request.POST['category']
            content = request.POST['content']
            info = request.POST['info']
            image = request.FILES.get('image')
            word_file = request.FILES.get('word_file')
            is_special = 'is_special' in request.POST
            is_trend = 'is_trend' in request.POST

            category = Category.objects.get(id=category_id)
            journalist = Journalist.objects.get(author=request.user)

            article = Article(
                journalist=journalist,
                title=title,
                info=info,
                content=content,
                word_file=word_file,
                category=category,
                image=image,
                is_special=is_special,
                is_trend=is_trend,
            )
            article.save()
            return redirect('dashboard')  # توجيه إلى صفحة المقالات أو أي وجهة أخرى

        context = {
            'today_str': today_str,
            'articles': articles,
            'today': today,
            'advertisment': advertisment,
            'categories': categories,
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "عذرا انت لست لديك الصلاحية للدخول لهذه الصفحة")
        return redirect('home')


def edit_article(request, pk):

    if request.user.is_authenticated and request.user.is_staff and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()

        article = get_object_or_404(Article, id=pk)
        if request.method == 'POST':

            title = request.POST['title']
            info = request.POST['info']
            content = request.POST['content']
            category_id = request.POST['category']
            image = request.FILES.get('image')
            word_file = request.FILES.get('word_file')
            is_special = 'is_special' in request.POST
            is_trend = 'is_trend' in request.POST

            category = Category.objects.get(id=category_id)

            # تحديث المقال
            article.title = title
            article.info = info
            article.content = content
            article.category = category
            article.image = image if image else article.image
            article.word_file = word_file if word_file else article.word_file
            article.is_special = is_special
            article.is_trend = is_trend
            article.save()

            messages.success(request, "تم تحديث المقال بنجاح")
            return redirect('dashboard')
        context = {
            'article': article,
            'categories': categories,
            'today_str':today_str,
            'today':today,
        }
        return render(request, 'parts/edit_article.html', context)
    else:
        messages.error(request, "عذرا انت لست لديك الصلاحية للدخول")
        return redirect('home')

def delete_article(request, pk):


    if request.user.is_authenticated and request.user.is_staff and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()

        article = get_object_or_404(Article, id=pk)

        if request.method =='POST':
            article.delete()
            messages.success(request, "تم حذف المقال بنجاح")
            return redirect('dashboard')
        context = {
            'article': article,
            'categories': categories,
            'today_str':today_str,
            'today':today,
        }
        return render(request, 'delete_article.html', context)
    else:
        messages.error(request, "عذرا انت لست لديك الصلاحية للدخول")
        return redirect('home')


def categories(request):

    cat_news = Article.objects.all().order_by('-add_date')

    special_news = Article.objects.filter(is_special=True).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date')
    categories = Category.objects.all()

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    advertisment = Advertisment.objects.all()

    context = {
        'cat_news':cat_news,
        'today_str': today_str,
        'special_news': special_news,
        'trending_news': trending_news,
        'categories': categories,
        'today': today,
        'advertisment': advertisment,
    }
    return render(request, 'categories.html', context)

def allcatnews(request, foo):

    foo = foo.replace("-", " ")
    articles = Article.objects.filter(category__name=foo).order_by('-add_date')

    special_news = Article.objects.filter(is_special=True).order_by('-add_date')
    trending_news = Article.objects.filter(is_trend=True).order_by('-add_date')
    categories = Category.objects.all()

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    advertisment = Advertisment.objects.all()

    context = {
        'foo':foo,
        'articles':articles,
        'today_str': today_str,
        'special_news': special_news,
        'trending_news': trending_news,
        'categories': categories,
        'today': today,
        'advertisment': advertisment,
    }
    return render(request, 'allcatnews.html', context)

def delete_com(request, pk):
        
    if request.user.is_authenticated and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()

        comment = get_object_or_404(Comment, id=pk)

        if request.method =='POST':
            comment.delete()
            messages.success(request, "تم حذف التعليق بنجاح")
            return redirect('news_page', pk=comment.article.id)
        context = {
            'comment': comment,
            'categories': categories,
            'today_str':today_str,
            'today':today,
        }
        return render(request, 'delete_com.html', context)
    else:
        messages.error(request, "عذرا انت لست لديك الصلاحية للدخول")
        return redirect('home')    



def add_category(request):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()

        if request.method == 'POST':
            category = request.POST.get('category')
            cat_photo = request.FILES.get('photo')
            if category and cat_photo:
                Category.objects.create(name=category, photo=cat_photo)
                messages.success(request, "تم اضافة الفئة بنجاح")
                return redirect('dashboard')
            else:
                messages.error(request, "عذرا يجب عليك ادخال جميع البيانات")
        context = {
            'categories': categories,
            'today_str':today_str,
            'today':today,
            }
        return render(request, 'add_category.html', context)


def contact_us(request):

    if request.user.is_authenticated and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()

        if request.method == 'POST':
            user = request.user
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            Contact.objects.create(user=user, name=name, email=email, phone=phone, subject=subject, message=message)
            messages.success(request, "شكرا لتواصلك معنا")
            return redirect('contact_us')
        context = {
            'now':now,
            'today':today,
            'today_str':today_str,
            'categories':categories,
        }
        return render(request, 'contact_us.html', context)
    else:
        messages.error(request, "رجاءً تسجيل الدخول اولا")
        return redirect('login')
    

def message(request):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_anonymous:
        now = timezone.now() + datetime.timedelta(hours=2)
        today = now.date()
        today_str = today.strftime("%A")
        categories = Category.objects.all()
        status = request.GET.get('status')
        if status == 'not_seen':
            contacts = Contact.objects.filter(is_viewd=False)
        elif status == 'seen':
            contacts = Contact.objects.filter(is_viewd=True) 
        elif status == 'all' or not status:
            contacts = Contact.objects.all()

        if 'search-bar' in request.GET:
            searched = request.GET['search-bar']
            if searched:
                # Filter products based on the search query
                contacts = contacts.filter(Q(name__icontains=searched) | Q(email__icontains=searched) | Q(phone__icontains=searched)|Q(subject__icontains=searched)| Q(message__icontains=searched)| Q(user__username__icontains=searched)| Q(user__first_name__icontains=searched)| Q(user__last_name__icontains=searched))
                if not allnews:
                    err = f'No results for {searched} \n Try checking your spelling or use more general terms'

        context = {
            'status':status,
            'contacts': contacts,
            'today':today,
            'today_str':today_str,
            'categories':categories,
            }
        return render(request, 'message.html', context)
    

def message_page (request, pk):
    message = get_object_or_404(Contact, pk=pk)
    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    categories = Category.objects.all()    
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_anonymous:
    # التحقق إذا كان المستخدم قد شاهد الرسالة من قبل
        if not message.viewed_by.filter(id=request.user.id).exists():
            # إذا لم يشاهد الرسالة من قبل، جدد الحالة
            message.viewed_by.add(request.user)
            message.is_viewd = True
            message.save(update_fields=['is_viewd'])
        context = {
            'contact': message,
            'today':today,
            'today_str':today_str,
            'categories':categories,
        }
        return render(request, 'message_page.html', context)


def delete_contact(request, pk):

    now = timezone.now() + datetime.timedelta(hours=2)
    today = now.date()
    today_str = today.strftime("%A")
    categories = Category.objects.all()    
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "تم حذف الرسالة بنجاح")
        return redirect('messages')
    context = {
        'contact': contact,
        'today':today,
        'today_str':today_str,
        'categories':categories,
        }
    return render(request, 'delete_contact.html', context)