from django.db import models
from api.models import User

class Daily_1m_content(models.Model):

    objects = models.Manager()

    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_1m_uid')
    time = models.CharField(null=True, max_length=20)
    type = models.CharField(max_length=2, null=True)


    def __str__(self):
        return str(self.time)


class Study_analysis(models.Model):     #새벽4시 일괄 업데이트

    objects = models.Manager()

    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_ana_uid')
    date = models.DateField(null=True)
    daily_concent_hour = models.IntegerField(null=True, default=0)
    daily_tot_hour = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.uid)


#어제날짜 없으면 one_week_study_data 생성하지 않게 하기 위해 
class today_date(models.Model):
    objects = models.Manager()
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='today_date_uid')
    day=models.DateField(null=True)

    def __str__(self):
        return str(self.day)

class One_week_study_data(models.Model):

    objects = models.Manager()

    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one_week_uid')
    day=models.DateField(null=True)
    date = models.CharField(null=True, max_length=10)
    concent_time = models.IntegerField(null=True, default=0)
    play_time = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.date)