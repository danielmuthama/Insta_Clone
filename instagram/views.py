from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import UserAccount
from .models import Comment, Post, Like

@login_required(login_url='login')
def home(request):
    name = request.GET.get('name') if request.GET.get('name') != None else ''

    user = UserAccount.objects.filter(Q(username__icontains = name)).order_by('-last_login')[0:6]
    
    post = Post.objects.all().order_by('-date_posted')
    post_comments = Comment.objects.all()
    context = {'post': post, 'post_comments': post_comments, 'user': user}
    return render(request, 'instagram/index.html', context)

@login_required(login_url='login')
def create_post(request):
    user = UserAccount.objects.all()
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')

        post = Post.objects.create(
            host = request.user,
            image = image,
            description = description
        )
        post.save()
        return redirect('home')
    return render(request, 'instagram/create_post.html', {'user': user})

@login_required(login_url='login')
def post_comment(request, post_id):
    user = UserAccount.objects.all()
    post = Post.objects.get(pk = post_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        print(comment)
        if comment is None:
            messages.error(request, "Comment can not be empty!")
        else :
            comments = Comment.objects.create(
                user = request.user,
                post = post,
                body = comment
            )
            # comments.save()
            return redirect('home')
    else: 
        print("invalid data")
    return render(request, 'instagram/index.html', {'user': user})
    
@login_required(login_url='login')
def like_post(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post')
        post_obj = Post.objects.get(id = post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else :
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if created:
            if like.value == 'like':
                like.value == 'unlike'
            else :
                like.value == 'like'
            
        like.save()    
    return redirect('home')
