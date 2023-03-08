import os
import googlemaps


API_KEY = os.environ['GOOGLE_GEOCODE_APIKEY']
G_MAPS = googlemaps.Client(key=API_KEY)


async def get_point(address):
    result = G_MAPS.geocode(address)

    if len(result) == 0:
        return None

    return {
        'formatted_address': result[0]['formatted_address'],
        'lat': result[0]['geometry']['location']['lat'],
        'lon': result[0]['geometry']['location']['lng']
    }
