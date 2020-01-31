# coding: utf-8

from django.conf import settings
import datetime, pytz 

from .shipper import ShipperWorkSpace
from codeshipper_app.models.update import Update

shippers = []

def workspace():
    now = datetime.datetime.now()
    now = now.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))

    updates_pending = Update.objects.filter(deploy_time__gte=now)

    for u in updates_pending:
        print("[update found]:", u)
        shippers.append(ShipperWorkSpace(u))

workspace()