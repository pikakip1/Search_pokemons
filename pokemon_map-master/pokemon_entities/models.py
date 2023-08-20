from datetime import timedelta

from django.db import models  # noqa F401

from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название покемона',
        )
    photo = models.ImageField(
        upload_to='pokemons_photo',
        verbose_name='Фото покемона',
        blank=True)

    eng_name = models.CharField(
        max_length=30,
        verbose_name='Перевод на английский',
        blank=True
    )

    jap_name = models.CharField(
        max_length=30,
        verbose_name='Перевод на японский',
        blank=True
    )

    description = models.CharField(
        max_length=1000,
        verbose_name='Описание',
        blank=True
    )

    evolution_from = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Эволюционировал из',
        related_name='next_evolution',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entity',
        verbose_name='Название покемона',
        )

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(verbose_name='Дата появления')
    disappeared_at = models.DateTimeField(
        verbose_name='Дата исчезновения',
    )

    level = models.IntegerField(verbose_name='Уровень', null=True,blank=True)
    health = models.IntegerField(verbose_name='Здоровье',null=True,blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True,blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True,blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    def __str__(self):
        return self.pokemon.title
