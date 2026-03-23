from django.db import models

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