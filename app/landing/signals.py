# -*- coding: utf-8 -*-
from robokassa.signals import result_received


def payment_received(sender, **kwargs):
    pass

result_received.connect(payment_received)
