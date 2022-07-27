from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from users.serializers import UserSerializer, RegistrationSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


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

