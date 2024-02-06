from django.urls import path
from cards import views

urlpatterns = [
    path(
        "",
        views.KCardListView.as_view(),
        name="k-card-list"
    ),

     path(
        "english",
        views.ECardListView.as_view(),
        name="e-card-list"
    ),
    path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),

    path(
        "edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
    ),

    path(
        "kbox/<str:box_name>",
        views.KoreanBoxView.as_view(),
        name="kbox"
    ),

     path(
        "ebox/<str:box_name>",
        views.EnglishBoxView.as_view(),
        name="ebox"
    ),

    path(
        "all-korean",
        views.KoreanTestAllView.as_view(),
        name="all-korean"
    ),

     path(
        "all-english",
        views.EnglishTestAllView.as_view(),
        name="all-english"
    ),
]