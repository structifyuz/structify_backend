from django.db import models
from django.utils import timezone

from base.managers import FlagsQuerySet, DeleteFlagQuerySet, ActiveFlagQuerySet


class TimeStampedModel(models.Model):
    """
    Models that have "created_at" and "created_user" fields
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )
    created_user = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_%(class)s_set',
        verbose_name='Создал'
    )

    # updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    class Meta:
        abstract = True


class DeleteFlagModel(models.Model):
    is_deleted = models.BooleanField(verbose_name='Удален', default=False)
    deleted_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        verbose_name="Дата удаления"
    )
    deleted_user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Удалил"
    )

    objects = DeleteFlagQuerySet.as_manager()
    query_set_class = DeleteFlagQuerySet

    class Meta:
        abstract = True


class ActiveFlagModel(models.Model):
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    objects = ActiveFlagQuerySet.as_manager()
    query_set_class = ActiveFlagQuerySet

    class Meta:
        abstract = True


class FlagsModel(models.Model):
    """
    Models that have active and deleted flags fields
    """
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_deleted = models.BooleanField(verbose_name='Удален', default=False)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата удаления"
    )
    deleted_user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='deleted_%(class)s_set',
        verbose_name="Удалил"
    )

    objects = FlagsQuerySet.as_manager()
    query_set_class = FlagsQuerySet

    class Meta:
        abstract = True

    def is_available(self):
        return (not self.is_deleted) and self.is_active

    def set_obj_deleted(self, user=None, save=True):
        self.is_active = False
        self.is_deleted = True
        self.deleted_user = user
        self.deleted_at = timezone.now()
        if save:
            self.save(update_fields=['is_active', 'is_deleted', 'deleted_user', 'deleted_at'])


class TimeStampedFlagsModel(FlagsModel, TimeStampedModel):
    class Meta:
        abstract = True
