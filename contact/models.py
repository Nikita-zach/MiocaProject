from django.db import models

class ContactMessage(models.Model):
    """
    Represents a message sent by a user through the contact form.

    Attributes:
        name (CharField): The name of the person sending the message.
        email (EmailField): The email address of the person sending the message.
        subject (CharField): The subject of the message.
        message (TextField): The content of the message.
        created_at (DateTimeField): The date and time when the message was created (auto-generated).

    Methods:
        __str__(self): Returns a string representation of the contact message, showing the sender's name and the subject.

    Example:
        contact_message = ContactMessage.objects.create(name="John Doe", email="john@example.com", subject="Inquiry", message="Hello!")
        print(contact_message)  # Output: "Message from John Doe - Inquiry"
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
