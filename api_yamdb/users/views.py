from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .permissions import IsAdmin
from .serializers import (UserSerializer,
                          RegistrationSerializer,
                          TokenSerializer)
from .utils import get_confirmation_code, check_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            user = request.user
            serializer = UserSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['role'] = user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def new_user(request):
    """Функция создания нового пользователя"""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        serializer.save()
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        send_mail(subject='New registration',
                  recipient_list=[serializer.validated_data.get('email')],
                  message=f'Your code: {get_confirmation_code(user)}',
                  from_email='email@email.ru',
                  fail_silently=False)
    except SMTPException as e:
        return Response({'error': e},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_token(request):
    """Функция получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if check_confirmation_code(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)
    else:
        return Response({'token': 'invalid token'},
                        status=status.HTTP_400_BAD_REQUEST)
