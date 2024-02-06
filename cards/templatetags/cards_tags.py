from django import template

from cards.models import Card
from django.utils import timezone
from datetime import timedelta

register = template.Library()

#code for the Korean boxes
@register.inclusion_tag("cards/k_box_links.html")
def k_boxes_as_links():
    boxes = []
    # Gets all unique box names assigned to cards
    unique_box_numbers = Card.objects.values_list('box', flat=True).distinct()

    # Gets number of eligible cards in each unique box
    for box_name in unique_box_numbers:
        threshold_time = timezone.now() - timedelta(minutes=30)
        eligible_count = Card.objects.filter(box=box_name, last_tested__lte=threshold_time).count()
        boxes.append({
            "number": box_name,
            "card_count": eligible_count,
        })

    return {"boxes": boxes}

#Code for the english boxes
@register.inclusion_tag("cards/e_box_links.html")
def e_boxes_as_links():
    boxes = []

    # Gets all unique box names assigned to cards
    unique_box_numbers = Card.objects.values_list('box', flat=True).distinct()

    # Gets number of eligible cards in each unique box
    for box_name in unique_box_numbers:
        threshold_time = timezone.now() - timedelta(minutes=30)
        eligible_count = Card.objects.filter(box=box_name, last_tested__lte=threshold_time).count()
        boxes.append({
            "number": box_name,
            "card_count": eligible_count,
        })

    return {"boxes": boxes}