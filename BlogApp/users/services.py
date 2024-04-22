from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .repository import CustomUserRepository, create_subscriber, save_subscriber
from .serializers import CreateCustomUserSerializer
from .models import CustomUser

User = get_user_model()


class CustomUserService:
    @staticmethod
    def create_user(user_data):
        existing_user = CustomUserRepository.get_by_name(user_data.get('username'))
        if existing_user:
            return {'user': None, 'error_message': 'Пользователь с таким именем уже существует'}

        serializer = CreateCustomUserSerializer(data=user_data)
        if serializer.is_valid():
            new_user = CustomUserRepository.create_user(serializer.validated_data)
            return {'user': new_user, 'error_message': None}
        else:
            return {'user': None, 'error_message': serializer.errors}

    @staticmethod
    def delete_user(user_id):
        existing_user = CustomUserRepository.get_by_id(user_id)
        if existing_user:
            deleted = CustomUserRepository.delete_user(existing_user.id)
            return {'deleted': deleted, 'reason': None}
        else:
            return {'deleted': False, 'reason': 'Пользователь не найден'}

    @staticmethod
    def update_user(user_id, data):
        existing_user = CustomUserRepository.get_by_id(user_id)
        if existing_user:
            updated_user = CustomUserRepository.update_user(user_id, data)
            if updated_user:
                return {'updated': True, 'user': updated_user, 'error_message': None}
            else:
                return {'updated': False, 'user': None, 'error_message': 'Ошибка при обновлении пользователя'}
        else:
            return {'updated': False, 'user': None, 'error_message': 'Пользователь не найден'}


def register_user(username, email, password):
    try:
        if User.objects.filter(username=username).exists():
            return False, "Пользователь с таким именем уже существует"
        if User.objects.filter(email=email).exists():
            return False, "Пользователь с таким email уже существует"

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return True, user
    except IntegrityError:
        return False, "Пользователь с таким email или именем уже существует"
    except Exception as e:
        return False, str(e)


def get_user_by_username(username):
    return get_object_or_404(CustomUser, username=username)


def subscribe_user(email):
    subscriber = create_subscriber(email)
    if subscriber:
        return True
    else:
        return False


def subscribe_user_to_newsletter(email):
    try:
        if User.objects.filter(email=email).exists():
            success, message = save_subscriber(email)
            return success, message
        else:
            return False, "User with this email does not exist."
    except Exception as e:
        return False, str(e)