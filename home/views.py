from django.shortcuts import render, redirect
from .models import Movie, Ticket, TicketHolder
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def auth_view(request):
    if request.method == 'POST':
        if 'login' in request.path:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Xác thực người dùng
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('movie_list')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login_signup.html', {'tab': 'login'})

        elif 'signup' in request.path:  # Nếu gửi từ /signup/
            username = request.POST.get('username')
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists.')
                    return render(request, 'login_signup.html', {'tab': 'signup'})
                else:
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        first_name=first_name, 
                        last_name=last_name)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Sign up successful! You are now logged in.')
                    return redirect('movie_list')
            else:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'login_signup.html', {'tab': 'signup'})

    return render(request, 'login_signup.html', {'tab': 'login'})

def logout_view(request):
    logout(request)  
    return redirect('movie_list')  

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})



@login_required(login_url='/login/')
def book_ticket(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    tickets = Ticket.objects.filter(movie=movie) 

    if request.method == 'POST':      
        ticket_type = request.POST['type']
        age = int(request.POST['age']) 
        ticket_id = request.POST['ticket'] 

        # Kiểm tra tuổi nhỏ hơn 2
        if age < 2:
            messages.error(request, 'Không có loại vé cho độ tuổi này.')
            return render(request, 'ticket_booking.html', {'movie': movie, 'tickets': tickets})

    
        if ticket_type.lower() == 'child': 
            if age > 12:
                messages.error(request, 'Children tickets are only available for ages 2 to 12.')
                return render(request, 'ticket_booking.html', {'movie': movie, 'tickets': tickets})

      
        selected_ticket = Ticket.objects.get(id=ticket_id)

        name = f"{request.user.first_name} {request.user.last_name}".strip() 
        # Tạo TicketHolder
        ticket_holder = TicketHolder(
            name=name,
            type=ticket_type,
            age=age,
            ticket=selected_ticket,
            user=request.user
        )
        ticket_holder.save()

        messages.success(request, 'Ticket booked successfully!')
        return redirect('movie_list')

    return render(request, 'ticket_booking.html', {'movie': movie, 'tickets': tickets})

@login_required(login_url='/login/')  # Đảm bảo người dùng phải đăng nhập
def my_bookings(request):
    if request.user.is_staff:  # Nếu là admin (is_staff=True)
        bookings = TicketHolder.objects.all()  # Lấy tất cả TicketHolder
    else:  # Nếu là user thường
        bookings = TicketHolder.objects.filter(user=request.user)  # Chỉ lấy vé của user hiện tại
    
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required(login_url='/login/')
def dashboard(request):
    # Dữ liệu tổng quan
    total_bookings = TicketHolder.objects.count()  # Tổng số vé đã đặt
    total_movies = Movie.objects.count()  # Tổng số phim
    user_bookings = TicketHolder.objects.filter(user=request.user).count()  # Số vé của user hiện tại
    movies = Movie.objects.all()  # Danh sách phim

    # Nếu là admin, lấy tất cả vé
    all_bookings = None
    if request.user.is_staff:
        all_bookings = TicketHolder.objects.all()

    context = {
        'total_bookings': total_bookings,
        'total_movies': total_movies,
        'user_bookings': user_bookings,
        'movies': movies,
        'all_bookings': all_bookings,
    }
    return render(request, 'dashboard.html', context)