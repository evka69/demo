from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, BookingForm, ReviewForm
from .models import UserProfile, Booking


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number']
            )
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'bookings': bookings})


@login_required
def create_booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})


@login_required
def submit_review_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения мероприятия')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за отзыв!')
            return redirect('dashboard')
    else:
        form = ReviewForm(instance=booking)

    return render(request, 'submit_review.html', {'form': form, 'booking': booking})


def is_admin_user(user):
    return user.username == 'Admin26' and user.is_authenticated


@user_passes_test(is_admin_user)
def admin_panel_view(request):
    bookings = Booking.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    sort_by = request.GET.get('sort', '-created_at')
    bookings = bookings.order_by(sort_by)

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = new_status
        booking.save()
        messages.success(request, f'Статус заявки #{booking_id} изменен')
        return redirect('admin_panel')

    return render(request, 'admin_panel.html', {'bookings': bookings, 'status_filter': status_filter})