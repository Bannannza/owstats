import requests
import json
from main import OWStats

bannannstats = OWStats('BANNANNZA-2257')

print('Current rank BANNANNZA is ' + str(bannannstats.get_current_rank()))
mas = input('Name: ')
print(mas)