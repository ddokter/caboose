from django.urls import path, include
from caboose.views.home import Home
from caboose.views.auth import LoginView, LogoutView
from caboose.views.base import (
    ListingView, CreateView, UpdateView, DeleteView, DetailView,
    InlineCreateView, InlineDeleteView, InlineUpdateView)
from caboose.views.recipe import (RecipeCreateView, RecipeUpdateView,
                                  RecipeConvertView)
from caboose.views.ship import ShipCreateView, ShipUpdateView
from caboose.views.event import (EventShoppingListView, EventCreateView,
                                 EventUpdateView)


urlpatterns = [

    path('auth/', include('django.contrib.auth.urls')),

    path('login/',
         LoginView.as_view(),
         name="login"),

    path('logout/',
         LogoutView.as_view(),
         name="logout"),

    path('', Home.as_view(), name="home"),

    # Non-generic views
    #
    path('recipe/add/',
         RecipeCreateView.as_view(),
         name="create_recipe"),

    path('recipe/<int:pk>/convert/',
         RecipeConvertView.as_view(),
         name="convert_recipe"),

    path('recipe/<int:pk>/edit',
         RecipeUpdateView.as_view(),
         name="edit_recipe"),

    path('ship/add/',
         ShipCreateView.as_view(),
         name="create_ship"),

    path('ship/<int:pk>/edit',
         ShipUpdateView.as_view(),
         name="edit_ship"),

    path('event/add/',
         EventCreateView.as_view(),
         name="create_event"),

    path('event/<int:pk>/edit',
         EventUpdateView.as_view(),
         name="edit_event"),

    path('event/<int:pk>/shopping_list',
         EventShoppingListView.as_view(),
         name="event_shopping_list"),

    # Generic delete view
    #
    path('<str:model>/<int:pk>/delete',
         DeleteView.as_view(),
         name="delete"),

    # Generic listing
    #
    path('<str:model>/list',
         ListingView.as_view(),
         name="list"),

    # Generic detail view
    #
    path('<str:model>/<int:pk>',
         DetailView.as_view(),
         name="view"),

    # Generic add view
    #
    path('<str:model>/add/',
         CreateView.as_view(),
         name="create"),

    # Generic edit view
    #
    path('<str:model>/<int:pk>/edit',
         UpdateView.as_view(),
         name="edit"),

    # Generic inline add
    #
    path('<str:parent_model>/<int:parent_pk>/add_<str:model>',
         InlineCreateView.as_view(),
         name="inline_create"),

    # Generic inline edit
    #
    path('<str:parent_model>/<int:parent_pk>/edit_<str:model>/<int:pk>',
         InlineUpdateView.as_view(),
         name="inline_edit"),

    # Generic inline delete
    #
    path('<str:parent_model>/<int:parent_pk>/rm_<str:model>/<int:pk>',
         InlineDeleteView.as_view(),
         name="inline_delete"),
]
