from datetime import datetime
from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import get_authorization_header

from apps.users.authentication import ExpiringTokenAuthentication
from apps.users.api.serializers.user_serializer import UserTokenSerializer

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request':request})
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data['user']

        if user.is_active:
            token,created = Token.objects.get_or_create(user=user)
            user_serializer = UserTokenSerializer(user)
            if created:
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message':'Inicio de sesion exitoso'
                }, status=status.HTTP_201_CREATED)
            
            else:
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                token = Token.objects.create(user=user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message':'Inicio de sesion exitoso'
                }, status=status.HTTP_201_CREATED)

        else:
            return Response({'mensaje':'este usuario no puede iniciar sesión'}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    
    def post(self, request, *args, **kwargs):

        try:
            token = request.POST.get('token')
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()
                session_message = 'Sesiones de usuario eliminadas'
                token_message = 'Token eliminado'
                return Response({'session_message':session_message, 'token_message':token_message}, status = status.HTTP_200_OK)
            
            return Response({'messagge': 'No se ha encontrado un usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({'error': 'No se ha encontrado el token en la petición'}, status=status.HTTP_409_CONFLICT)
        


class VerifyTokenView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        token = get_authorization_header(request).split()
        print("Token recibido en VerifyTokenView:", token)  # 👈 Aquí verás tu print

        if not token or len(token) != 2:
            return Response({'valid': False, 'error': 'Formato inválido'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user, _ = ExpiringTokenAuthentication().authenticate_credentials(token[1].decode())
            return Response({
                'valid': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        except Exception as e:
            return Response({'valid': False, 'error': str(e), 'mensaje':'por alguna razon falló'},
                            status=status.HTTP_401_UNAUTHORIZED)