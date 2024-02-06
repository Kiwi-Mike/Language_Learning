from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
import random
from datetime import timedelta
from django.utils import timezone
from .forms import CardCheckForm

# Create your views here.
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)

from .models import Card

#View for seeing all cards with korean first, ordered by box and then last tested time
class KCardListView(ListView):
    model = Card
    #defining which html file to use
    template_name = "cards/k_card_list.html"
    queryset = Card.objects.all().order_by("box", "-last_tested")

#View for seeing all cards with english first, ordered by box and then last tested time
class ECardListView(ListView):
    model = Card
    #defining which html file to use
    template_name = "cards/e_card_list.html"
    queryset = Card.objects.all().order_by("box", "-last_tested")

#View for creating a new card with required fields, loads self after creating card
class CardCreateView(CreateView):
    model = Card
    fields = ["korean", "english", "box"]
    success_url = reverse_lazy("card-create")

#View for updating a card, loads korean first view after updating
class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("k-card-list")

#View for testing all cards with Korean showing
class KoreanTestAllView(KCardListView):
    #defining which html file to use
    template_name = "cards/all_korean_box.html"

    def get_queryset(self):
        return Card.objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object_list:
            cards = Card.objects.all()
                        
            if cards:
                #All cards are eligible as testing for all
                eligible_cards = [card for card in cards]
                #Shuffle order of cards so random each time
                random.shuffle(eligible_cards)

                #Defining required attributes so html is loaded correctly
                context["eligible_cards"] = eligible_cards
                context["all_check_card"] = True


        return context
    
#View for testing all cards with Korean showing 
class EnglishTestAllView(KCardListView):

    #defining which html file to use
    template_name = "cards/all_english_box.html"

    def get_queryset(self):
        return Card.objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object_list:
            cards = Card.objects.all()
                        
            if cards:
                #All cards are eligible as testing all cards
                eligible_cards = [card for card in cards]\
                #Shuffling the order so view is random each time
                random.shuffle(eligible_cards)

                #Defining variables to html is loaded correctly
                context["eligible_cards"] = eligible_cards
                context["all_check_card"] = True


        return context

#View for testing all cards in a box with the korean showing
class KoreanBoxView(KCardListView):
    #html file to read
    template_name = "cards/box.html"

    #form for updating card eligibility if word is known
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_name"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Defining variables to html is loaded correctly
        context["box_number"] = self.kwargs["box_name"]


        if self.object_list:
            #Checking whether the card was solved in the last 30 minutes
            eligible_cards = [card for card in self.object_list if self.is_card_eligible(card)]

            if eligible_cards:
                #randomly choosing a card from the eligible cards to test
                context["check_card"] = random.choice(eligible_cards)
                context["eligible_cards"] = eligible_cards

        return context

    def post(self, request, *args, **kwargs):

        #checking whether user input 'I know' or 'I don't know'
        is_true = request.POST.get("solved") == "True"

        form = self.form_class(request.POST)

        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])

            #Updating last_tested if solved else do nothing and keep in box
            if is_true:
                card.last_tested = timezone.now()
                card.save()

        #reload the page after posting, else load 'k-card-list'
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        else:
            return redirect('k-card-list')

    #Checks whether has been solved in the last 30 minutes
    def is_card_eligible(self, card):
        threshold_time = timezone.now() - timedelta(minutes=30)
        return card.last_tested <= threshold_time

#View for testing all cards in a box with the english showing
class EnglishBoxView(ECardListView):
    #which html file to use
    template_name = "cards/k_box.html"

    #form for updating card eligibility if word is known
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_name"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Defining variables to html is loaded correctly
        context["box_number"] = self.kwargs["box_name"]

        
        if self.object_list:
            #only loading cards that have not been solved in last 30 minutes
            eligible_cards = [card for card in self.object_list if self.is_card_eligible(card)]

            if eligible_cards:
                #showing a random card from the eligible cards list
                context["check_card"] = random.choice(eligible_cards)
                context["eligible_cards"] = eligible_cards

        return context

    def post(self, request, *args, **kwargs):

        is_true = request.POST.get("solved") == "True"

        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])

            if is_true:
                card.last_tested = timezone.now()
                card.save()

        
        #reload the page after posting, else load 'k-card-list'
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        else:
            return redirect('k-card-list')
    
    #Checks whether has been solved in the last 30 minutes
    def is_card_eligible(self, card):
        threshold_time = timezone.now() - timedelta(minutes=30)
        return card.last_tested <= threshold_time