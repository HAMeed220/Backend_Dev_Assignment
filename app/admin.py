from django.contrib import admin

# Register your models here.
# Importing models from the 'app' module, which likely contains database models
from app.models import *

# Registering the CustomUser model with the admin site, allowing administrators to manage users
admin.site.register(CustomUser)

# Registering the Paragraph model with the admin site, enabling administrators to manage paragraphs
admin.site.register(Paragraph)

# Registering the ParagraphWord model with the admin site, allowing administrators to manage relationships between paragraphs and words
admin.site.register(ParagraphWord)

# Registering the Word model with the admin site, enabling administrators to manage individual words
admin.site.register(Word)