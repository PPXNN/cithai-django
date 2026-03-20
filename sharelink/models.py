from django.db import models

# Create your models here.
class Sharelink(models.Model):

    song = models.OneToOneField(
        "song.Song", 
        on_delete=models.CASCADE,
        related_name="share_link"
    )
    url = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "share_link"

    def __str__(self):
        return f"{self.song}, {self.url}"
