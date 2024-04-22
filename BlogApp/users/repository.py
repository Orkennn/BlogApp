from django.contrib.auth import get_user_model

from .models import CustomUser
from .models import Subscriber
User = get_user_model()


class CustomUserRepository:
    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_name(name):
        try:
            return CustomUser.objects.get(name=name)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def create_user(data):
        new_user = CustomUser.objects.create(**data)
        return new_user

    @staticmethod
    def update_user(user_id, data):
        user = CustomUserRepository.get_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            return user
        else:
            return None

    @staticmethod
    def delete_user(user_id):
        user = CustomUserRepository.get_by_id(user_id)
        if user:
            user.delete()
            return True
        else:
            return False


def create_subscriber(email):
    try:
        subscriber = Subscriber.objects.create(email=email)
        return subscriber
    except Exception as e:
        print(f"Failed to create subscriber: {e}")
        return None


def save_subscriber(email):
    try:
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if Subscriber.objects.filter(user=user).exists():
                return False, "Subscriber with this Email already exists."

            subscriber = Subscriber.objects.create(user=user)
            subscriber.save()
            return True, "Subscriber added successfully."
        else:
            return False, "User with this email does not exist."
    except Exception as e:
        return False, str(e)
