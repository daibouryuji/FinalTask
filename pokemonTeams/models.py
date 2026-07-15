from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Team(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="teams"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TeamPokemon(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="pokemons"
    )

    slot = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6),
        ]
    )

    name = models.CharField(max_length=20, blank=True)

    image = models.ImageField(
        upload_to="pokemon/",
        blank=True,
        null=True
    )

    item = models.CharField(max_length=10, blank=True)
    ability = models.CharField(max_length=10, blank=True)
    nature = models.CharField(max_length=10, blank=True)

    h_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    a_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    b_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    c_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    d_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    s_Status = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(32)]
    )

    move1 = models.CharField(max_length=30, blank=True)
    move2 = models.CharField(max_length=30, blank=True)
    move3 = models.CharField(max_length=30, blank=True)
    move4 = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["slot"]
        unique_together = ("team", "slot")