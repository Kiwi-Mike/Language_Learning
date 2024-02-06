from django.test import TestCase
from django.urls import reverse
from .models import Card
from .views import EnglishBoxView
from datetime import timedelta
from django.utils import timezone
from .forms import CardCheckForm

# Create your tests here.
class BasicTest(TestCase):

    form_class = CardCheckForm

    def test_fields(self):
        card = Card()
        card.english = "hello"
        card.korean = "안녕"
        card.box = "Greetings"
        card.save()

        record = Card.objects.get(pk=1)
        self.assertEqual(record, card)

    def test_is_eligible_card(self):
        card = Card()
        card.english = "hello"
        card.korean = "안녕"
        card.box = "Greetings"
        card.save()

        card.last_tested = timezone.now() - timedelta(minutes=31)

        self.assertTrue(EnglishBoxView.is_card_eligible(self, card))

    def test_is_not_eligible_card(self):
        card = Card()
        card.english = "hello"
        card.korean = "안녕"
        card.box = "Greetings"
        card.save()

        self.assertFalse(EnglishBoxView.is_card_eligible(self, card))

    def test_update_last_tested(self):
        card = Card()
        card.english = "hello"
        card.korean = "안녕"
        card.box = "Greetings"
        card.save()

        url = reverse('ebox', args=[card.box])

        new_value = timezone.now()
        response = self.client.post(url, {'solved': 'True'})

        self.assertEqual(response.status_code, 302)

        tolerance = timedelta(seconds=1)

        self.assertAlmostEqual(card.last_tested, new_value, delta=tolerance)

class UrlsTest(TestCase):

    def test_k_card_list_url(self):
        url = reverse('k-card-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/k_card_list.html')

    def test_e_card_list_url(self):
        url = reverse('e-card-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/e_card_list.html')



