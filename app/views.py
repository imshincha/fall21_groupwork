from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.models import User
from .models import Paper, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PaperForm
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    papers = Paper.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'papers': papers})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    papers = user.paper_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'papers':papers})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Userインスタンスを作成
        if form.is_valid():
            form.save() # Userインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければNoneを返す
            new_user = authenticate(
                username=input_username,
                password=input_password,
                )
            # 認証成功時のみ、ユーザーをログインさせる
            if new_user is not None:
            # login関数は、認証ができてなくてもログインさせることができる。(認証は上のauthenticateで実行する)
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def papers_new(request):
    if request.method == "POST":
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.user = request.user
            paper.save()
            messages.success(request, "投稿が完了しました!")
        return redirect('app:users_detail', pk=request.user.pk)
    else:
        form = PaperForm()
    return render(request, 'app/papers_new.html', {'form': form})

def papers_detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    return render(request, 'app/papers_detail.html', {'paper': paper})

@require_POST
def papers_delete(request, pk):
    paper = get_object_or_404(Paper, pk=pk, user=request.user)
    paper.delete()
    return redirect('app:users_detail', request.user.id)

def papers_category(request, category):
# titleがURLの文字列と一致するCategoryインスタンスを取得
    category = get_object_or_404(Category, title=category)
    # 取得したCategoryに属するPaper一覧を取得
    papers = Paper.objects.filter(category=category).order_by('-created_at')
    return render(
        request, 'app/index.html', {'papers': papers, 'category': category}
    )