from rest_framework import generics,viewsets ,views, response, status
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.exceptions import ValidationError

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        # Django's logout function will remove the authenticated user's ID from the session and flush their session data.
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class accountsView(viewsets.ModelViewSet):
    serializer_class = CustomUserModelSerializer
    queryset = CustomUserModel.objects.all() 
class DetailseView(viewsets.ModelViewSet):
    serializer_class = CustomUserDetailsSerializer
    queryset = CustomUserDetails.objects.all() 
                       
                        
class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        # You can provide a message or any data you want to return on GET request
        return Response({'message': 'Please send a POST request with username and password.'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # You can include any additional data in the response here
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ServiceAvailabilityView(views.APIView):
    def get(self, request, *args, **kwargs):
        now = timezone.localtime(timezone.now()).time()
        try:
            service_id = kwargs.get('service_id')
            service = CustomUserDetails.objects.get(pk=service_id)
            # Check if current time is within the opening and closing times
            if service.opening_time <= now <= service.closing_time:
                return response.Response({'available': True}, status=status.HTTP_200_OK)
            else:
                return response.Response({'available': False}, status=status.HTTP_200_OK)
        except CustomUserDetails.DoesNotExist:
            return response.Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ServiceBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        service_name = self.kwargs['service_name']
        return Booking.objects.filter(service=service_name)
    
class ServiceInquiryView(generics.ListAPIView):
    serializer_class = CustomUserDetailsSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        service_type = self.request.query_params.get('service_type')
        radius_km = self.radius_km  # Use the instance variable set in the list method

        if latitude is None or longitude is None:
            raise ValidationError("Latitude and longitude are required parameters.")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise ValidationError("Latitude and longitude must be valid numbers.")

        # Haversine formula to calculate distance
        queryset = CustomUserDetails.objects.annotate(
            distance=ACos(
                Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) *
                Cos(Radians(F('longitude')) - Radians(longitude)) +
                Sin(Radians(latitude)) * Sin(Radians(F('latitude')))
            ) * 6371  # Radius of Earth in kilometers
        ).filter(distance__lte=radius_km)

        if service_type:
            queryset = queryset.filter(service_type=service_type)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            # Initial search within 5km
            self.radius_km = 5
            queryset = self.get_queryset()
            if not queryset.exists():
                # If no results, search within 10km
                self.radius_km = 10
                queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "An unexpected error occurred: " + str(e)}, status=500)