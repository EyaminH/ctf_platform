from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from challenges.models import Submission

from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    solved_count = submissions.filter(is_correct=True).count()
    authored_challenges = request.user.authored_challenges.all().order_by('-created_at')
    
    return render(request, 'users/dashboard.html', {
        'submissions': submissions,
        'solved_count': solved_count,
        'authored_challenges': authored_challenges
    })
