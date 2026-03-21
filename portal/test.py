from django.contrib.auth.models import User
from .models import EventSuggestion

class EventSuggestionModelTest():
    
    def test_create_event_suggestion(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        
        suggestion = EventSuggestion.objects.create(
            user=user,
            title='Test Event',
            location='Dublin',
            start_datetime='2030-07-01 10:00:00',
            status = "PENDING"
        )
        self.assertEqual(suggestion.title, 'Test Event')