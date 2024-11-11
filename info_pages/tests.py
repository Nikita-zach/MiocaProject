from django.test import TestCase
from django.urls import reverse
from .models import FAQ, ServiceSection, Stuff, Testimonials, BrandIcons, Feature
from django.core.files.uploadedfile import SimpleUploadedFile


class FAQModelTest(TestCase):
    """
    Tests for the FAQ model to ensure that FAQ entries are correctly created and
    the string representation of the FAQ object works as expected.
    """

    def test_faq_model_creation(self):
        """
        Test that a FAQ object is created correctly with question and answer.
        Verifies if the object is stored correctly in the database.
        """
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework."
        )
        self.assertEqual(faq.question, "What is Django?")
        self.assertEqual(faq.answer, "Django is a Python web framework.")

    def test_faq_str(self):
        """
        Test the __str__ method of the FAQ model. This method should return the question
        when called on a FAQ object.
        """
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework."
        )
        self.assertEqual(str(faq), "What is Django?")


class ServiceSectionModelTest(TestCase):
    """
    Tests for the ServiceSection model to ensure the fields are correctly populated and
    that the __str__ method returns the expected value.
    """

    def test_service_section_model_creation(self):
        """
        Test that a ServiceSection object is created with an image, title, subtitles,
        and mission statements. Checks that the object is stored properly in the database.
        """
        image = SimpleUploadedFile(name="image.jpg", content=b"file_content", content_type="image/jpeg")
        service_section = ServiceSection.objects.create(
            image=image,
            shape=image,
            title="Our Services",
            subtitle_1="Subtitle 1",
            subtitle_2="Subtitle 2",
            our_mission1="Mission 1",
            our_mission2="Mission 2"
        )
        self.assertEqual(service_section.title, "Our Services")
        self.assertEqual(service_section.subtitle_1, "Subtitle 1")
        self.assertEqual(service_section.our_mission1, "Mission 1")

    def test_service_section_str(self):
        """
        Test the __str__ method of the ServiceSection model. It should return the title
        of the ServiceSection when called.
        """
        service_section = ServiceSection.objects.create(
            title="Our Services",
            subtitle_1="Subtitle 1",
            subtitle_2="Subtitle 2",
            our_mission1="Mission 1",
            our_mission2="Mission 2"
        )
        self.assertEqual(str(service_section), "Our Services")


class StuffModelTest(TestCase):
    """
    Tests for the Stuff model to verify that staff members can be created and that
    the string representation works as expected.
    """

    def test_stuff_model_creation(self):
        """
        Test that a Stuff object can be created with a name and profession,
        and that it is saved correctly in the database.
        """
        staff_member = Stuff.objects.create(
            name="John Doe",
            profession="Developer",
            is_visible=True
        )
        self.assertEqual(staff_member.name, "John Doe")
        self.assertEqual(staff_member.profession, "Developer")

    def test_stuff_str(self):
        """
        Test the __str__ method of the Stuff model. It should return the name of the staff
        member when called on a Stuff object.
        """
        staff_member = Stuff.objects.create(
            name="John Doe",
            profession="Developer"
        )
        self.assertEqual(str(staff_member), "John Doe")


class TestimonialsModelTest(TestCase):
    """
    Tests for the Testimonials model to verify that testimonial entries are correctly created
    and the string representation of the testimonial object works as expected.
    """

    def test_testimonials_model_creation(self):
        """
        Test that a Testimonials object is created with a name and description,
        and it is stored correctly in the database.
        """
        testimonial = Testimonials.objects.create(
            name="Jane Smith",
            description="Great service!",
        )
        self.assertEqual(testimonial.name, "Jane Smith")
        self.assertEqual(testimonial.description, "Great service!")

    def test_testimonials_str(self):
        """
        Test the __str__ method of the Testimonials model. It should return the name of
        the testimonial when called on a Testimonials object.
        """
        testimonial = Testimonials.objects.create(
            name="Jane Smith",
            description="Great service!"
        )
        self.assertEqual(str(testimonial), "Jane Smith")


class BrandIconsModelTest(TestCase):
    """
    Tests for the BrandIcons model to ensure that the brand icons are created correctly
    with an image and stored properly.
    """

    def test_brand_icons_model_creation(self):
        """
        Test that a BrandIcons object is created with an image and is saved properly in the database.
        """
        image = SimpleUploadedFile(name="brand_icon.jpg", content=b"file_content", content_type="image/jpeg")
        brand_icon = BrandIcons.objects.create(image=image)
        self.assertTrue(brand_icon.image.name.endswith("brand_icon.jpg"))

    def test_brand_icons_creation(self):
        """
        Test that the 'created_at' field is populated when a BrandIcons object is created.
        """
        brand_icon = BrandIcons.objects.create(image="partners/brand_icon.jpg")
        self.assertIsNotNone(brand_icon.created_at)


class FeatureModelTest(TestCase):
    """
    Tests for the Feature model to ensure that feature entries are correctly created
    and the string representation of the feature object works as expected.
    """

    def test_feature_model_creation(self):
        """
        Test that a Feature object is created with a name, description, and image,
        and that it is correctly saved in the database.
        """
        image = SimpleUploadedFile(name="feature_image.jpg", content=b"file_content", content_type="image/jpeg")
        feature = Feature.objects.create(
            name="Feature 1",
            description="Description of Feature 1",
            image=image
        )
        self.assertEqual(feature.name, "Feature 1")
        self.assertEqual(feature.description, "Description of Feature 1")

    def test_feature_str(self):
        """
        Test the __str__ method of the Feature model. It should return the name of the feature
        when called on a Feature object.
        """
        feature = Feature.objects.create(
            name="Feature 1",
            description="Description of Feature 1"
        )
        self.assertEqual(str(feature), "Feature 1")


class AboutPageViewTest(TestCase):
    """
    Tests for the about_page view to ensure that the page loads correctly and
    passes the correct context data to the template.
    """

    def test_about_page_view(self):
        """
        Test that the about page view returns a 200 status code, uses the correct template,
        and passes the necessary context variables to the template.
        """
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertIn('service_section', response.context)
        self.assertIn('features', response.context)
        self.assertIn('team', response.context)
        self.assertIn('testimonials', response.context)
        self.assertIn('brands', response.context)


class FAQViewTest(TestCase):
    """
    Tests for the faq_view to ensure that the FAQ page loads correctly and
    displays all FAQ entries.
    """

    def test_faq_view(self):
        """
        Test that the FAQ view renders the correct template, returns a 200 status code,
        and passes all FAQ entries to the template.
        """
        FAQ.objects.create(question="What is Django?", answer="Django is a Python framework.")
        response = self.client.get(reverse('faq_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        self.assertIn('faqs', response.context)
        self.assertEqual(len(response.context['faqs']), 1)


class PrivacyPolicyViewTest(TestCase):
    """
    Tests for the privacy policy page to ensure it loads correctly and uses the proper template.
    """

    def test_privacy_policy_view(self):
        """
        Test that the privacy policy page renders correctly and returns a 200 status code.
        """
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy-policy.html')


class Custom404ViewTest(TestCase):
    """
    Tests for the custom 404 error page to ensure it renders the correct template.
    """

    def test_custom_404_view(self):
        """
        Test that accessing a non-existent page renders the custom 404 error page with
        a 404 status code.
        """
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')