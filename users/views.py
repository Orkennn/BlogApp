from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import SubscribeForm
from .models import Subscriber
from .services import CustomUserService, get_user_by_username, subscribe_user_to_newsletter
from .serializers import CreateCustomUserSerializer
from .services import register_user
from django.urls import reverse


class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user, error_message = CustomUserService.create_user(serializer.validated_data)
            if new_user:
                return Response({'user': new_user}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    def delete(self, request, user_id):
        result = CustomUserService.delete_user(user_id)
        if result['deleted']:
            return Response({'message': 'Пользователь успешно удален'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': result['reason']}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserView(APIView):
    def put(self, request, user_id):
        serializer = CreateCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            updated, user, error_message = CustomUserService.update_user(user_id, serializer.validated_data)
            if updated:
                return Response({'user': user}, status=status.HTTP_200_OK)
            else:
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        success, result = register_user(username, email, password)
        if success:
            return redirect('profile', username=username)
        else:
            error_message = result
            return render(request, 'registration.html', {'error_message': error_message})
    else:
        registration_url = reverse('register')
        return render(request, 'registration.html', {'registration_url': registration_url})


@login_required()
def profile_view(request, username):
    user = get_user_by_username(username)
    return render(request, 'profile.html', {'user': user})


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно подписались на нашу рассылку!')
            return redirect('post-list')
    else:
        form = SubscribeForm()
    return render(request, 'subscribe.html', {'form': form})


def subscribe_user_to_newsletter_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            success, message = subscribe_user_to_newsletter(email)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect('post-list')
    else:
        form = SubscribeForm()
    return render(request, 'subscribe.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')
