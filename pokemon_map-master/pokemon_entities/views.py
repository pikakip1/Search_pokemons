import folium

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

    moscow_time = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entity = PokemonEntity.objects.filter(
        disappeared_at__gt=moscow_time,
        appeared_at__lt=moscow_time
    )

    for pokemon_entity in pokemon_entity:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []

    for pokemon in all_pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def get_evolution(pokemon, request):
    evolution = {}
    if pokemon:
        evolution['title_ru'] = pokemon
        evolution['pokemon_id'] = pokemon.id
        evolution['img_url'] = request.build_absolute_uri(pokemon.photo.url)
    return evolution


def show_pokemon(request, pokemon_id):
    pokemon_cards = PokemonEntity.objects.filter(pokemon_id=pokemon_id)

    pokemon_card = pokemon_cards[0].pokemon.pokemon_entity.first().pokemon

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_cards:
        pokemon_img = pokemon_entity.pokemon.pokemon_entity.first().pokemon.photo.url
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_img)
        )

    next_evolution_pokemon = get_evolution(pokemon_card.next_evolution.all().first(), request)
    previous_evolution_pokemon = get_evolution(pokemon_card.evolution_from, request)

    pokemon_card = {
        'pokemon_id': pokemon_card.id,
        'title_ru': pokemon_card.title,
        'img_url': request.build_absolute_uri(pokemon_card.photo.url),
        'description': pokemon_card.description,
        'title_en': pokemon_card.eng_name,
        'title_jp': pokemon_card.jap_name,
        'previous_evolution': dict(previous_evolution_pokemon),
        'next_evolution': dict(next_evolution_pokemon)
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_card
    })
