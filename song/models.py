from django.db import models


# Create your models here.
class Song(models.Model):
    class Occasion(models.TextChoices):
        BIRTHDAY = "birthday", "birthday"
        WEDDING = "wedding", "wedding"
        ANNIVERSARY = "anniversary", "anniversary"
        HOLIDAY = "holiday", "holiday"
        OTHER = "other", "other"
    
    class Genre(models.TextChoices):
        POP = "pop", "pop"
        ROCK = "rock", "rock"
        JAZZ = "jazz", "jazz"
        CLASSICAL = "classical", "classical"
        HIPHOP = "hiphop", "hiphop"
        RB = "rb", "rb"
        FOLK = "folk", "folk"
    
    class VoiceType(models.TextChoices):
        MALE = "male", "male"
        FEMALE = "female", "female"
        INSTRUMENTAL = "instrumental", "instrumental"
    
    class Mood(models.TextChoices):
        HAPPY = "happy", "happy"
        SAD = "sad", "sad"
        ROMANTIC = "romantic", "romantic"
        CALM = "calm", "calm"
        FUNNY = "funny", "funny"
    
    class SongStatus(models.TextChoices):
        GENERATING = "generating", "generating"
        COMPLETED = "completed", "completed"
        FAILED = "failed", "failed"

    user = models.ForeignKey(
        "user.User",
        on_delete= models.CASCADE,
        related_name="song"
        )
    
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    occasion = models.CharField(max_length=20, choices=Occasion.choices, default=Occasion.OTHER)
    genre = models.CharField(max_length=10, choices=Genre.choices, default=Genre.POP)
    voice_type = models.CharField(max_length=13, choices=VoiceType.choices, default=VoiceType.MALE)
    mood = models.CharField(max_length=10, choices=Mood.choices, default=Mood.HAPPY)
    status = models.CharField(max_length=11, choices=SongStatus.choices, default=SongStatus.GENERATING)
    audiofile_url = models.CharField(max_length=500, blank=True, default="")
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "song"
    
    def __str__(self):
        return f"{self.title} {self.description}"

