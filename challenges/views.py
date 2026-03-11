from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from .models import Challenge, Category, Submission
from django.contrib.auth.models import User
from users.models import Profile

def home(request):
    challenges = Challenge.objects.filter(is_approved=True).order_by('-created_at')[:3]
    return render(request, 'home.html', {'challenges': challenges})

@login_required
def challenge_list(request):
    categories = Category.objects.all()
    challenges = Challenge.objects.filter(is_approved=True)
    solved_challenges = Submission.objects.filter(user=request.user, is_correct=True).values_list('challenge_id', flat=True)
    
    return render(request, 'challenges/challenge_list.html', {
        'categories': categories,
        'challenges': challenges,
        'solved_challenges': solved_challenges
    })

@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    already_solved = Submission.objects.filter(user=request.user, challenge=challenge, is_correct=True).exists()
    
    if request.method == 'POST':
        if already_solved:
            messages.warning(request, "You have already solved this challenge.")
            return redirect('challenge_detail', pk=pk)
            
        submitted_flag = request.POST.get('flag')
        is_correct = (submitted_flag == challenge.flag)
        
        Submission.objects.create(
            user=request.user,
            challenge=challenge,
            submitted_flag=submitted_flag,
            is_correct=is_correct
        )
        
        if is_correct:
            profile = request.user.profile
            profile.total_score += challenge.points
            profile.save()
            messages.success(request, f"Correct! You earned {challenge.points} points.")
            return redirect('challenge_list')
        else:
            messages.error(request, "Incorrect flag. Try again.")
            
    return render(request, 'challenges/challenge_detail.html', {
        'challenge': challenge,
        'already_solved': already_solved
    })

def leaderboard(request):
    top_profiles = Profile.objects.select_related('user').order_by('-total_score')[:10]
    return render(request, 'challenges/leaderboard.html', {'profiles': top_profiles})

@login_required
def submit_challenge_user(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        points = request.POST.get('points')
        flag = request.POST.get('flag')
        category_id = request.POST.get('category')
        
        category = get_object_or_404(Category, id=category_id)
        
        Challenge.objects.create(
            title=title,
            description=description,
            points=points,
            flag=flag,
            author=request.user,
            category=category,
            status='PENDING',
            is_approved=False
        )
        messages.success(request, "Challenge submitted! It will appear on the platform once approved by an admin.")
        return redirect('dashboard')
        
    categories = Category.objects.all()
    return render(request, 'challenges/submit_challenge.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
def admin_review_list(request):
    pending_challenges = Challenge.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'challenges/admin_review.html', {
        'pending_challenges': pending_challenges
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    return render(request, 'challenges/admin_challenge_detail.html', {
        'challenge': challenge
    })

@user_passes_test(lambda u: u.is_superuser)
def approve_challenge(request, pk):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, pk=pk)
        challenge.is_approved = True
        challenge.status = 'APPROVED'
        challenge.save()
        messages.success(request, f"Challenge '{challenge.title}' has been approved.")
    return redirect('admin_review')

@user_passes_test(lambda u: u.is_superuser)
def reject_challenge(request, pk):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, pk=pk)
        rejection_reason = request.POST.get('rejection_reason')
        challenge.status = 'REJECTED'
        challenge.is_approved = False
        challenge.rejection_reason = rejection_reason
        challenge.save()
        messages.warning(request, f"Challenge '{challenge.title}' has been rejected.")
    return redirect('admin_review')
