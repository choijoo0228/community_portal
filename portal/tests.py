from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import EventSuggestion


class EventSuggestionModelTest(TestCase):

    def test_create_event_suggestion(self):
        user = User.objects.create_user(username="testuser", password="testpass")

        suggestion = EventSuggestion.objects.create(
            user=user,
            title="Test Event",
            location="Dublin",
            start_datetime=timezone.make_aware(datetime(2030, 7, 1, 10, 0, 0)),
            status="PENDING",
        )

        self.assertEqual(suggestion.title, "Test Event")