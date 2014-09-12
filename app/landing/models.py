# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_NEW = 0
    STATUS_PAID = 10
    STATUS_FAIL = 100

    STATUS_CHOICES = (
        (STATUS_NEW, u'Создан счет'),
        (STATUS_PAID, u'Счет оплачен'),
        (STATUS_FAIL, u'Ошибка оплаты'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', verbose_name=u'Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
    sum = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name=u'Cумма')
    status = models.IntegerField(default=STATUS_NEW, choices=STATUS_CHOICES, verbose_name=u'Статус')
    description = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name=u'Описание')

    class Meta:
        verbose_name = u'платеж'
        verbose_name_plural = u'платежи'
        ordering = ('-date',)
