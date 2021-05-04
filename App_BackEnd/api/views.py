from rest_framework import generics, permissions, views, response,status
from .models import Account
from .serializers import signupSerializer, AccountSerializer, loginSerializer



# Create your views here.


class signup(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = signupSerializer
    permission_classes = [permissions.AllowAny]

"""
class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
"""



class login(views.APIView):
    queryset = Account.objects.all()
    serializer_class = loginSerializer

    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_date = serializer.data
            return response.Response(new_date,status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)