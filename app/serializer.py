# Import necessary modules from Django Rest Framework
from rest_framework import serializers

# Import models from the current app
from.models import CustomUser, Paragraph, Word,ParagraphWord

# Define a serializer for login functionality
class LoginSerializer(serializers.Serializer):
    # Email field for user login
    email = serializers.EmailField()
    # Password field for user login, with input type set to password for security
    password = serializers.CharField(style={'input_type': 'password'})

# Define a serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    # Meta class to define metadata for the serializer
    class Meta:
        # Specify the model to serialize
        model = CustomUser
        # Include all fields from the model in the serializer
        fields = '__all__'

# Define a serializer for Paragraph model
class ParagraphSerializer(serializers.ModelSerializer):
    # Meta class to define metadata for the serializer
    class Meta:
        # Specify the model to serialize
        model = Paragraph
        # Include all fields from the model in the serializer
        fields = '__all__'
    
class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphWord
        fields =  '__all__' # other fields...

# Define a serializer for Word model
class WordSerializer(serializers.ModelSerializer):
    # Meta class to define metadata for the serializer
    class Meta:
        # Specify the model to serialize
        model = Word
        # Include all fields from the model in the serializer
        fields = '__all__'
