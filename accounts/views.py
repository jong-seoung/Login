from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import SignUpForm


class SignUpAPIView(APIView):
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
