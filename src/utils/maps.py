import os
import googlemaps


API_KEY = os.environ['GOOGLE_GEOCODE_APIKEY']
G_MAPS = googlemaps.Client(key=API_KEY)


async def get_point(address):
    results = G_MAPS.places(address)['results']

    if len(results) == 0:
        return None

    return {
        'formatted_address': results[0]['formatted_address'],
        'lat': results[0]['geometry']['location']['lat'],
        'lon': results[0]['geometry']['location']['lng']
    }
