from geopy.geocoders import Nominatim
'''
class Geolocation:
    def __init__(self):
'''

geolocator = Nominatim(user_agent="UHopperInternship")

#From coordinates get Location
location = geolocator.reverse("46.128851,11.128102")

print(location.raw['address']['city'])