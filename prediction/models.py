from django.db import models
from django.contrib.auth.models import User


class UserHistory(models.Model):
    related_user = models.ForeignKey(User,  on_delete=models.CASCADE)
    uploaded_img_url = models.URLField()
    number_of_leaf = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'Number of leaves : {} in this image : {}'.format(
            self.number_of_leaf, self.uploaded_img_url
        )