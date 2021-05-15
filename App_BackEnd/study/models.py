from django.db import models
from api.models import User

class Daily_1m_content(models.Model):

    objects = models.Manager()

    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_1m_uid')
    datetime = models.DateTimeField(null=True)

    CONC = (
        ('C', 'Concentrate'),
        ('P', 'Play'),
        ('U', 'Unknown'),
    )
    concentrate = models.CharField(max_length=2, choices=CONC, null=True)

    def __str__(self):
        return str(self.concentrate)


class Study_analysis(models.Model):     #새벽4시 일괄 업데이트

    objects = models.Manager()

    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_ana_uid')
    date = models.DateField(null=True)
    daily_concent_hour = models.FloatField(null=True)
    daily_tot_hour = models.FloatField(null=True)

    def __str__(self):
        return str(self.daily_concent_hour)





