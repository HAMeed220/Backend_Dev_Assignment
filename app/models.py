# Import the AbstractUser model from Django's built-in auth module
from django.contrib.auth.models import AbstractUser
# Import the models module from Django's db module
from django.db import models

# Define a custom user model that inherits from AbstractUser
class CustomUser(AbstractUser):
    # Add a date of birth field to the custom user model
    CustomUser_dob = models.DateField(null=True, blank=True)
    # Add a created at field to the custom user model, automatically set to the current date and time when the user is created
    CustomUser_created_at = models.DateTimeField(auto_now_add=True)
    # Add a modified at field to the custom user model, automatically set to the current date and time when the user is modified
    CustomUser_modified_at = models.DateTimeField(auto_now=True)

    # Define the many-to-many relationship between the custom user and groups
    groups = models.ManyToManyField(
        # The related model is the built-in Group model from Django's auth module
        to='auth.Group',
        # The related name is the name of the relationship from the Group model back to the CustomUser model
        related_name='custom_users',
        # Allow blank values in the database
        blank=True,
        # Help text for the field in the admin interface
        help_text=('The groups this user belongs to. A user will get all permissions '
                    'from all of the groups they are promiscuous in.'),
        # Verbose name for the field in the admin interface
        verbose_name='groups',
        # Related query name for the relationship
        related_query_name='custom_user',
    )
    # Define the many-to-many relationship between the custom user and permissions
    user_permissions = models.ManyToManyField(
        # The related model is the built-in Permission model from Django's auth module
        to='auth.Permission',
        # The related name is the name of the relationship from the Permission model back to the CustomUser model
        related_name='custom_users',
        # Allow blank values in the database
        blank=True,
        # Help text for the field in the admin interface
        help_text=('The permissions granted to this user.'),
        # Verbose name for the field in the admin interface
        verbose_name='user permissions',
    )


# Define a custom manager for the Paragraph model
class ParagraphManager(models.Manager):
    # Define a method to create a new paragraph
    def create_paragraph(self, text):
        # Create a new paragraph instance with the given text
        pm_paragraph = self.model(text=text)
        # Save the paragraph to the database
        pm_paragraph.save(force_insert=True)
        # Index the paragraph by creating ParagraphWord instances for each word
        self._index_paragraph(pm_paragraph)
        # Return the created paragraph
        return pm_paragraph
    
    # Define a method to index a paragraph by creating ParagraphWord instances for each word
    def _index_paragraph(self, paragraph):
        # Split the paragraph text into individual words
        words = paragraph.text.lower().split()
        # Iterate over each word
        for word in words:
            # Get or create a ParagraphWord instance for the word and paragraph
            ParagraphWord.objects.get_or_create(
                paragraph=paragraph,
                word=word
            )


# Define the Paragraph model
class Paragraph(models.Model):
    # Define the primary key field for the paragraph
    Paragraph_id = models.AutoField(primary_key=True)
    # Define the text field for the paragraph
    Paragraph_text = models.TextField()
    # Define the created at field for the paragraph, automatically set to the current date and time when the paragraph is created
    Paragraph_created_at = models.DateTimeField(auto_now_add=True)
    # Define the modified at field for the paragraph, automatically set to the current date and time when the paragraph is modified
    Paragraph_modified_at = models.DateTimeField(auto_now=True)
    # Define the custom manager for the Paragraph model
    Paragraph_objects = ParagraphManager()
    
    # Define the string representation of the paragraph
    def __str__(self):
        return self.Paragraph_text


# Define the ParagraphWord model
class ParagraphWord(models.Model):
    # Define the foreign key field to the Paragraph model
    pw_paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    # Define the word field
    pw_word = models.CharField(max_length=355)
    # Define a unique constraint on the paragraph and word fields
    class Meta:
        unique_together = ('pw_paragraph', 'pw_word')
    
    # Define the string representation of the paragraph word
    def __str__(self):
        return self.pw_word


# Define the Word model
class Word(models.Model):
    # Define the primary key field for the word
    Word_id = models.AutoField(primary_key=True)
    # Define the text field for the word
    Word_text = models.CharField(max_length=355)
    # Define the foreign key field to the Paragraph model
    Word_paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    # Define the created at field for the word, automatically set to the current date and time when the word is created
    Word_created_at = models.DateTimeField(auto_now_add=True)
    # Define the modified at field for the word, automatically set to the current date and time when the word is modified
    Word_modified_at = models.DateTimeField(auto_now=True)

    # Define the string representation of the word
    def __str__(self):
        return self.Word_text
