# coding: utf-8

from django.conf import settings
import datetime, pytz 

from .shipper import ShipperWorkSpace
from codeshipper_app.models.updating import Updating

shippers = []

def workspace():
    now = datetime.datetime.now()
    now = now.astimezone(pytz.timezone(pytz.country_timezones("VN")[0]))

    updates_pending = Updating.objects.filter(deploy_time__gte=now)

    for u in updates_pending:
        print("[updating found]:", u)
        shippers.append(ShipperWorkSpace(u))

workspace()