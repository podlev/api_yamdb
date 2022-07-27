from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from users.serializers import UserSerializer, RegistrationSerializer, TokenSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False, permission_classes=(IsAuthenticated,))
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
def new_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        send_mail(subject='New registration',
                  recipient_list=[serializer.validated_data.get('email')],
                  message=f'Token: 000000',
                  from_email='email@email.ru',
                  fail_silently=False)
        serializer.save()
    except SMTPException as e:
        return Response({'Ошибка отправки email': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    else:
        return Response({'Ошибка': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
