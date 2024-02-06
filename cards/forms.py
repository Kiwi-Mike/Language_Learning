from django import forms

# Form for checking cards, either know or don't know. Form always needs a card but doesn't need answer
class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)