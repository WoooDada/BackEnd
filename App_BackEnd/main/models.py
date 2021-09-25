from django.db import models
from api.models import User
from django.contrib.postgres.fields import ArrayField

class Room(models.Model):

    maker_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='f_maker')
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100, null=False)
    maxppl = models.IntegerField(default=2)
    is_secret = models.BooleanField()
    room_pwd = models.CharField(max_length=10, null=True, blank=True)
    room_tag = models.CharField(max_length=50, null=True, blank=True)
    room_comment = models.CharField(max_length=2000, null=True, blank=True)
    room_color = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.room_name)



class Room_Enroll(models.Model):

    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='f_room')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='f_uid')
    current = models.BooleanField(null=True, blank=True)
    room_color = models.CharField(max_length=10)

    def __str__(self):
        return str(self.room_id)


class Recent_Room(models.Model) :


    room_array = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)