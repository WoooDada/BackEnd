from django.db import models


class Daily_1m_concent(models.Models) :

    uid = models.ForeignKey("User",related_name="uid", on_delete=models.CASCADE,db_column="uid")
    datetime = models.DateTimeField(auto_now=True)
            #Daily-1m-concent.save()될 때마다 작동하고 자동으로 수정됨.
            #query문 update되어도 이 필드는 수정안됨.
    concent_field = (
        ('C', 'concentrate'),
        ('P', 'play'),
        ('U', 'unknown'),
    )
    concentrate = models.CharField(max_length=2, choices=concent_field)

