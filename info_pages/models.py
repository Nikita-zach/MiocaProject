from django.db import models


class FAQ(models.Model):
    """
    Represents a frequently asked question displayed on the FAQ page.

    - Each FAQ contains a question and its answer.
    - This model tracks timestamps for creation and updates.

    Fields:
        question (CharField): The text of the FAQ question.
        answer (CharField): The text answer to the question.
        created_at (DateTimeField): Timestamp when the FAQ was created.
        updated_at (DateTimeField): Timestamp when the FAQ was last updated.
    """
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question


class ServiceSection(models.Model):
    """
    Represents a service section, often displayed on an 'About Us' page.

    - This model includes information about a specific service, with images, title, and mission details.
    - Also tracks timestamps for creation and updates.

    Fields:
        image (ImageField): Main image for the service section.
        shape (ImageField): Shape image associated with the service.
        title (CharField): Title of the service section.
        subtitle_1 (CharField): First subtitle or short description.
        subtitle_2 (CharField): Second subtitle or short description.
        our_mission1 (CharField): Part one of the mission statement.
        our_mission2 (CharField): Part two of the mission statement.
        created_at (DateTimeField): Timestamp when the service section was created.
        updated_at (DateTimeField): Timestamp when the service section was last updated.
    """
    image = models.ImageField(upload_to='images/')
    shape = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    subtitle_1 = models.CharField(max_length=255)
    subtitle_2 = models.CharField(max_length=255)
    our_mission1 = models.CharField(max_length=255)
    our_mission2 = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Stuff(models.Model):
    """
    Represents a team member or staff profile, displayed on team pages.

    - Each staff member has a unique name, profession, and photo.
    - The model includes sorting and visibility controls.

    Fields:
        name (CharField): The staff member's name, unique for each instance.
        profession (CharField): The profession or title of the staff member, unique.
        photo (ImageField): Photo of the staff member.
        sort (IntegerField): Determines the display order for staff members.
        is_visible (BooleanField): Controls visibility on the front end.
        created (DateTimeField): Timestamp when the staff member was created.
        updated (DateTimeField): Timestamp when the staff member was last updated.
    """
    name = models.CharField(max_length=50, unique=True)
    profession = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='stuffs/')

    sort = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Testimonials(models.Model):
    """
    Represents a testimonial entry, typically displayed in testimonial sections on the site.

    - Each testimonial includes the name, photo, and description of the testimonial.
    - This model tracks timestamps for creation and updates.

    Fields:
        name (CharField): Name of the individual providing the testimonial, unique.
        photo (ImageField): Photo of the individual giving the testimonial.
        description (CharField): Text of the testimonial.
        created_at (DateTimeField): Timestamp when the testimonial was created.
        updated_at (DateTimeField): Timestamp when the testimonial was last updated.
    """
    name = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='testimonials/')
    description = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class BrandIcons(models.Model):
    """
    Represents brand icons displayed in the brand section, often on the homepage.

    - Each icon represents a partner or associated brand's logo.
    - This model tracks timestamps for creation and updates.

    Fields:
        image (ImageField): Image file for the brand icon.
        created_at (DateTimeField): Timestamp when the brand icon was created.
        updated_at (DateTimeField): Timestamp when the brand icon was last updated.
    """
    image = models.ImageField(upload_to='partners/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
