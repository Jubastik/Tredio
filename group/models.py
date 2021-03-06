from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from group.querysets import MeetupParticipantQuerySet, MeetupQuerySet
from theatres.models import Event

User = get_user_model()


class Meetup(models.Model):
    host = models.ForeignKey(User, verbose_name="Организатор", on_delete=models.CASCADE, related_name="meetups")
    event = models.ForeignKey(Event, verbose_name="Событие", on_delete=models.CASCADE, related_name="meetups")
    start = models.DateTimeField(verbose_name="Время встречи")
    participants_limit = models.IntegerField(
        "Максимальное кол-во участников", validators=[MinValueValidator(1)], null=True, blank=True
    )
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)

    objects = models.Manager()
    meetups = MeetupQuerySet.as_manager()

    def is_participant(self, user: User):
        return (
            user == self.host or MeetupParticipant.meetup_participants.fetch_by_meetup(self).filter(user=user).exists()
        )

    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"


class MeetupParticipant(models.Model):
    meetup = models.ForeignKey(Meetup, verbose_name="Встреча", related_name="participants", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Участник", on_delete=models.CASCADE)

    objects = models.Manager()
    meetup_participants = MeetupParticipantQuerySet.as_manager()

    class Meta:
        verbose_name = "Участник встречи"
        verbose_name_plural = "Участники встреч"
