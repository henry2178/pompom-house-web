from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
import stripe
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

stripe.api_key = os.environ.get('STRIPE_API_KEY', 'sk_test_fake_key_for_local_dev')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            role = form.cleaned_data.get('role')
            if role == 'student':
                user.is_student = True
            elif role == 'landlord':
                user.is_landlord = True

            user.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            authenticated_user = authenticate(
                request,
                username=email,
                password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)

            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'pompom/register.html', {'form': form})


def home_view(request):
    query = request.GET.get('q', '')

    if query:
        all_properties = Property.objects.filter(
            Q(title__icontains=query) |
            Q(landlord__first_name__icontains=query) |
            Q(landlord__last_name__icontains=query) |
            Q(landlord__username__icontains=query)
        ).order_by('-id')
    else:
        all_properties = Property.objects.all().order_by('-id')

    total_count = all_properties.count()

    paginator = Paginator(all_properties, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_count': total_count,
        'query': query,
    }
    return render(request, 'pompom/home.html', context)

def property_detail_view(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'pompom/property_detail.html', {'property': property})

@login_required
def login_redirect_view(request):
    # if non-student
    if getattr(request.user, 'is_landlord', False):
        return redirect('landlord_dashboard')
    # if student
    else:
        return redirect('home')

@login_required
def toggle_favorite_view(request, property_id):
    if request.method == 'POST':
        prop = get_object_or_404(Property, id=property_id)

        if request.user in prop.favorites.all():
            prop.favorites.remove(request.user)
            is_favorited = False
        else:
            prop.favorites.add(request.user)
            is_favorited = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'is_favorited': is_favorited})

        return redirect('property_detail', property_id=prop.id)

@login_required
def my_favorites_view(request):
    favorite_properties = request.user.favorite_properties.all()
    return render(request, 'pompom/my_favorites.html', {'properties': favorite_properties})


@login_required
def update_personal_info_view(request):
    if request.method == 'POST':
        user = request.user
        action = request.POST.get('action')

        if action == 'update_name':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()

        elif action == 'update_email':
            user.email = request.POST.get('email', user.email)
            user.username = request.POST.get('email', user.username)
            user.save()

        elif action == 'update_phone':
            user.phone = request.POST.get('phone', user.phone)
            user.save()

        elif action == 'update_password':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def create_booking_view(request, property_id):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, id=property_id)
        weeks = int(request.POST.get('weeks', 1))
        total_price = property_obj.price * weeks

        Booking.objects.create(
            property=property_obj,
            tenant=request.user,
            weeks=weeks,
            total_price=total_price,
            status='Pending'
        )
        return redirect('my_bookings')

    return redirect('property_detail', property_id=property_id)

@login_required
def my_bookings_view(request):
    bookings = request.user.bookings.all().order_by('-created_time')
    return render(request, 'pompom/my_bookings.html', {'bookings': bookings})


# cancel order
@login_required
def cancel_booking_view(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, tenant=request.user)

        if booking.status == 'Pending':
            booking.status = 'Cancelled'
            booking.save()

    return redirect('my_bookings')

# landlord view
@login_required
def landlord_dashboard_view(request):
    if not getattr(request.user, 'is_landlord', False):
        return redirect('home')

    my_properties = Property.objects.filter(landlord=request.user).order_by('-id')

    incoming_bookings = Booking.objects.filter(property__landlord=request.user).order_by('-created_time')

    context = {
        'properties': my_properties,
        'bookings': incoming_bookings,
    }
    return render(request, 'pompom/landlord_dashboard.html', context)


# manage oder(for landlord)
@login_required
def process_booking_view(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, property__landlord=request.user)

        action = request.POST.get('action')

        if booking.status == 'Pending':
            if action == 'approve':
                booking.status = 'Approved'
            elif action == 'reject':
                booking.status = 'Rejected'
            booking.save()

    return redirect('landlord_dashboard')

# add property
@login_required
def add_property_view(request):
    if not getattr(request.user, 'is_landlord', False):
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        address = request.POST.get('address')
        price = request.POST.get('price')
        description = request.POST.get('description')

        photo = request.FILES.get('photo')

        bed_type = request.POST.get('bed_type', 'Double Bed', )
        bathroom_type = request.POST.get('bathroom_type', 'Shared')

        rating = request.POST.get('rating', 5.0)
        review_count = request.POST.get('review_count', 0)

        Property.objects.create(
            landlord=request.user,
            title=title,
            address=address,
            price=price,
            description=description,
            bed_type=bed_type,
            bathroom_type=bathroom_type,
            photo=photo,
            rating=rating,
            review_count=review_count
        )

        return redirect('landlord_dashboard')

    return render(request, 'pompom/add_property.html')

# delete property
@login_required
def delete_property_view(request, property_id):
    if request.method == 'POST':
        property_to_delete = get_object_or_404(Property, id=property_id, landlord=request.user)
        property_to_delete.delete()

    return redirect('landlord_dashboard')


# landlord can edit their own property
@login_required
def edit_property_view(request, property_id):
    prop = get_object_or_404(Property, id=property_id, landlord=request.user)

    if request.method == 'POST':
        prop.title = request.POST.get('title')
        prop.address = request.POST.get('address')
        prop.price = request.POST.get('price')
        prop.description = request.POST.get('description')
        prop.bed_type = request.POST.get('bed_type')
        prop.bathroom_type = request.POST.get('bathroom_type')
        prop.rating = request.POST.get('rating', prop.rating)
        prop.review_count = request.POST.get('review_count', prop.review_count)

        if 'photo' in request.FILES:
            prop.photo = request.FILES['photo']

        prop.save()

        return redirect('landlord_dashboard')

    return render(request, 'pompom/edit_property.html', {'property': prop})

# payment
@login_required
def create_checkout_session_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tenant=request.user, status='Approved')

    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': int(booking.total_price * 100),
                        'product_data': {
                            'name': f"Booking for {booking.property.title}",
                            'description': f"Duration: {booking.weeks} Weeks",
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/my-bookings/'),
            cancel_url=request.build_absolute_uri('/my-bookings/'),
        )
        return redirect(checkout_session.url, code=303)

    return redirect('my_bookings')