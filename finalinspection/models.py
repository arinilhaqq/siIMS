from django.db import models
from appointment.models import Appointment

KONDISI_INTERIOR = (('W', 'Worn'),
               ('B', 'Burns'),
               ('R', 'Ripped'),
               ('S', 'Stain'),
               ('C', 'Cracked'))

class FinalInspection(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    # informasi kendaraan awal
    front_1 = models.BooleanField(default=False)
    front_2 = models.BooleanField(default=False)
    front_3 = models.BooleanField(default=False)
    front_4 = models.BooleanField(default=False)
    front_5 = models.BooleanField(default=False)
    back_6 = models.BooleanField(default=False)
    back_7 = models.BooleanField(default=False)
    back_8 = models.BooleanField(default=False)
    back_9 = models.BooleanField(default=False)
    back_10 = models.BooleanField(default=False)
    passenger_11 = models.BooleanField(default=False)
    passenger_12 = models.BooleanField(default=False)
    passenger_13 = models.BooleanField(default=False)
    passenger_14 = models.BooleanField(default=False)
    passenger_15 = models.BooleanField(default=False)
    passenger_16 = models.BooleanField(default=False)
    passenger_17 = models.BooleanField(default=False)
    passenger_18 = models.BooleanField(default=False)
    passenger_19 = models.BooleanField(default=False)
    top_20 = models.BooleanField(default=False)
    top_21 = models.BooleanField(default=False)
    top_22 = models.BooleanField(default=False)
    top_23 = models.BooleanField(default=False)
    driver_24 = models.BooleanField(default=False)
    driver_25 = models.BooleanField(default=False)
    driver_26 = models.BooleanField(default=False)
    driver_27 = models.BooleanField(default=False)
    driver_28 = models.BooleanField(default=False)
    driver_29 = models.BooleanField(default=False)
    driver_30 = models.BooleanField(default=False)
    driver_31 = models.BooleanField(default=False)
    driver_32 = models.BooleanField(default=False)
    catatan = models.TextField(blank=True, null=True)
    karpet = models.CharField(choices=KONDISI_INTERIOR, default='', max_length=50, blank=True, null=True)
    kursi = models.CharField(choices=KONDISI_INTERIOR, default='', max_length=50, blank=True, null=True)
    headliner = models.CharField(choices=KONDISI_INTERIOR, default='', max_length=50, blank=True, null=True)
    door_panels = models.CharField(choices=KONDISI_INTERIOR, default='', max_length=50, blank=True, null=True)

    checked = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
