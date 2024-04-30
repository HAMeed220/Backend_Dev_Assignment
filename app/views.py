from django.shortcuts import render
# Import necessary modules from Django and REST framework
# Create your views here.
from app.serializer import CustomUserSerializer, ParagraphSerializer, WordSerializer, LoginSerializer
# Import custom serializers for models
from app.models import CustomUser, Paragraph, Word, ParagraphWord
# Import custom models
from rest_framework.response import Response
# Import Response object from REST framework
from rest_framework.views import APIView
# Import APIView class from REST framework
from rest_framework import status, views, permissions, authentication
# Import various modules from REST framework
from rest_framework.authtoken.models import Token
# Import Token model from REST framework
from rest_framework import viewsets
# Import viewsets module from REST framework


class LoginView(views.APIView):
    # Define a view for handling login requests
    permission_classes = [permissions.AllowAny]
    # Allow any user to access this view
    serializer_class = LoginSerializer
    # Specify the serializer to use for this view
    permission_classes = [permissions.AllowAny]
    # Allow any user to access this view

    def post(self, request):
        # Handle POST requests to this view
        email = request.data.get('email')
        # Get the email from the request data
        password = request.data.get('password')
        # Get the password from the request data
        if not email or not password:
            # Check if either email or password is missing
            return Response({'error': 'Both email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
            # Return an error response if either field is missing
        user = authentication(email=email, password=password)
        # Authenticate the user using the provided email and password
        if user is None:
            # Check if the authentication failed
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
            # Return an error response if the authentication failed
        token, created = Token.objects.get_or_create(user=user)
        # Get or create a token for the authenticated user
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})
        # Return a response with the token, user ID, and email


class ParagraphView(APIView):
    # Define a view for handling paragraph creation
    def post(self, request):
        # Handle POST requests to this view
        paragraphs = request.data.get('paragraphs')
        # Get the list of paragraphs from the request data
        for paragraph in paragraphs:
            # Iterate over each paragraph
            paragraph_obj = Paragraph(text=paragraph)
            # Create a new Paragraph object with the provided text
            paragraph_obj.save()
            # Save the Paragraph object to the database
            words = paragraph.split()
            # Split the paragraph into individual words
            for word in words:
                # Iterate over each word
                word_obj = Word(text=word.lower(), paragraph=paragraph_obj)
                # Create a new Word object with the provided text and paragraph
                word_obj.save()
                # Save the Word object to the database
        return Response({'message': 'Paragraphs saved successfully'})
        # Return a success response


class SearchView(APIView):
    # Define a view for handling search requests
    def get(self, request):
        # Handle GET requests to this view
        word = request.query_params.get('word')
        # Get the search word from the query parameters
        words = Word.objects.filter(text=word.lower())
        # Get the list of Word objects that match the search word
        paragraphs = [word.paragraph for word in words]
        # Get the list of Paragraph objects associated with the matching words
        serializer = ParagraphSerializer(paragraphs, many=True)
        # Serialize the list of Paragraph objects
        return Response(serializer.data)
        # Return a response with the serialized data


class CustomUserViewSet(viewsets.ModelViewSet):
    # Define a viewset for handling CustomUser model
    queryset = CustomUser.objects.all()
    # Specify the queryset for this viewset
    serializer_class = CustomUserSerializer
    # Specify the serializer to use for this viewset


class ParagraphViewSet(viewsets.ModelViewSet):
    # Define a viewset for handling ParagraphWord model
    queryset = ParagraphWord.objects.all()
    # Specify the queryset for this viewset
    serializer_class = ParagraphSerializer
    # Specify the serializer to use for this viewset


class WordViewSet(viewsets.ModelViewSet):
    # Define a viewset for handling Word model
    queryset = Word.objects.all()
    # Specify the queryset for this viewset
    serializer_class = WordSerializer
    # Specify the serializer to use for this viewset