from django.db import models
from api.models import User





class Monthly_tdl(models.Model):


    objects = models.Manager()
    m_todo_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Monthly_tdl_uid')
    stt_date = models.DateField(null=False)
    end_date = models.DateField()
    m_content = models.TextField(max_length=100)

    def __str__(self):
        return str(self.m_todo_id)






class Weekly_tdl(models.Model):


    objects = models.Manager()

    w_todo_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Weekly_tdl_uid')
    w_date = models.DateField()
    w_content = models.TextField(max_length=100)
    w_check = models.BooleanField()

    def __str__(self):
        return str(self.w_todo_id)



class Daily_tdl(models.Model):

    objects = models.Manager()

    d_todo_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Daily_tdl_uid')
    d_date = models.DateField()
    d_tag = models.TextField(max_length=20, null=True)
    d_content = models.TextField(max_length=100)
    d_check = models.BooleanField()

    def __str__(self):
        return str(self.d_todo_id)
