from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='pokemons_photo', blank=True)

    translate_name = {
        'Бульбазавр':
            {
                "title_en": "Bulbasaur",
                "title_jp": "フシギダネ"
            },

        'Ивизавр':
            {
                "title_en": "Ivysaur",
                "title_jp": "フシギソウ",
            },

        'Венузавр':
            {
                "title_en": "Venusaur",
                "title_jp": "フシギバナ",
            }
    }

    BULVASAUR_DESCRIPTION = '''
            cтартовый покемон двойного травяного и ядовитого типа из первого поколения и региона\
            Канто. В национальном покедексе под номером 1. На 16 уровне эволюционирует в Ивизавра. Ивизавр на 32\
            уровне эволюционирует в Венузавра. Наряду с Чармандером и Сквиртлом, Бульбазавр является\
            одним из трёх стартовых покемонов региона Канто.\
        '''

    IVIZAUR_DESCRIPTION = '''
            покемон двойного травяного и ядовитого типа из первого поколения покемонов. Эволюционирует из стартового\
            покемона Бульбазавра на 16 уровне. Становится Венузавром на 32 уровне.
    '''

    VENUZAUR_DESCRIPTION = '''
            покемон двойного травяного и ядовитого типа из первого поколения покемонов. На 32 уровне эволюционирует из\
            Ивизавра. Финальная эволюция травяного стартовика Бульбазавра. Развивается в Мега Венузавра с помощью камня\
            Венусарита.
    '''

    DESCRIPTION = {
        'Бульбазавр': BULVASAUR_DESCRIPTION,
        'Ивизавр': IVIZAUR_DESCRIPTION,
        'Венузавр': VENUZAUR_DESCRIPTION
    }

    evolution_from = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, blank=True)

    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=100)
    defence = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)

    def __str__(self):
        return self.pokemon.title
