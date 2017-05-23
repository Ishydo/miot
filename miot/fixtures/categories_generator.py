from slugify import slugify

place_index = 1;
places_categories = [
          "Airport",
          "Amusement Park",
          "Art Gallery",
          "ATM",
          "Bakery",
          "Bank",
          "Bar",
          "Beauty Salon",
          "Bicycle Store",
          "Bowling",
          "Bus Station",
          "Cafe",
          "Casino",
          "Clothing Store",
          "Florist",
          "Food",
          "Gas Station",
          "Gym",
          "Haircare",
          "Hospital",
          "Jewelry Store",
          "Library",
          "Meal Takeaway",
          "Movie Theater",
          "Museum",
          "Night Club",
          "Park",
          "Parking",
          "Pharmacy",
          "Restaurant",
          "School",
          "Shopping Mall",
          "Stadium",
          "Store",
          "Train Station",
          "University",
          "Zoo",
]

str = ""

for i, pc in enumerate(places_categories):
    str += '''{{
          'model': 'miot.category',
          'pk': {0},
          'fields': {{
            'name': '{1}',
            'slug': '{2}',
            'emoji_name': null,
            'short_description': 'A place.',
            'parent': 1
          }}
        }},'''.format(i+place_index+1, pc, slugify(pc))

print(str.replace("\'", "\""))
