import folium
import json
import pytz

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    all_pokemons = Pokemon.objects.all()

    moscow_time = timezone.localtime(timezone=pytz.timezone('Europe/Moscow'))
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in all_pokemons:

        for pokemon_entity in PokemonEntity.objects.filter(
            pokemon=pokemon,
            disappeared_at__gt=moscow_time,
            appeared_at__lt=moscow_time
        ):

            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.photo.url)
            )

    pokemons_on_page = []

    for pokemon in all_pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else '',
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url)
        )

    if pokemon.title == 'Венузавр':
        evolution = 'Ивизавр'

    else:
        evolution = 'Бульбазавр'

    pokemon_previous_evolution = Pokemon.objects.filter(title=evolution).last()
    print(pokemon.evolution_)

    pokemon_card = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'img_url': request.build_absolute_uri(pokemon.photo.url),
        'description': pokemon.DESCRIPTION[pokemon.title],
        'title_en': pokemon.translate_name[pokemon.title]['title_en'],
        'title_jp': pokemon.translate_name[pokemon.title]['title_jp'],
        'previous_evolution': {
            'title_ru': pokemon_previous_evolution,
            "pokemon_id": pokemon_previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon_previous_evolution.photo.url)

        }
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_card
    })
