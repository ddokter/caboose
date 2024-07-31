""" Register event handlers for Django's signals """

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .event import Event, EventService
from .task import Task


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, **kwargs):

    Task.objects.create(name=f"{ instance } - Personeel")


@receiver(m2m_changed, sender=EventService)
def eventservice_m2m_changed(instance, sender, **kwargs):

    for service in instance.list_services():
        Task.objects.create(
            name=f"{ instance } - { service }"
        )
