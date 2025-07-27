from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from rooms.models import Room


def reviews_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/reviews.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        room_id = request.POST.get('room')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        room = None
        if room_id:
            room = Room.objects.get(id=room_id)
        
        review = Review(
            user=request.user,
            category=category,
            room=room,
            rating=rating,
            comment=comment
        )
        review.save()
        
        messages.success(request, 'Thank you for your review!')
        return redirect('reviews')
    
    rooms = Room.objects.all()
    category_choices = Review.CATEGORY_CHOICES
    rating_choices = Review.RATING_CHOICES
    
    return render(request, 'reviews/add_review.html', {
        'rooms': rooms,
        'category_choices': category_choices,
        'rating_choices': rating_choices
    })