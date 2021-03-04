## GpxReader
Parse GPX file (e.g. OsmAnd [favourites.gpx](example-files/favourites.gpx)) and turn waypoints (aka wpt nodes) into Python dictionary structure.
** Example usage **
```
from GpxReader import OsmandFavouritesReader

for poi in OsmandFavouritesReader('favourites.gpx'):
    print(poi)
```
And the output looks like:
```
{'latitude': '43.2363701', 'longitude': '76.9615479', 'name': '"European" Backpackers Hostel', 'type': 'stayed overnight', 'cmt': 'Amenity:"European" Backpackers Hostel: man_made:building', 'osmand': {'color': '#b41010a0'}}
{'latitude': '41.7000777', 'longitude': '44.7990923', 'name': 'Another POI', 'type': 'POI', 'osmand': {'color': '#b41010a0'}}
```
