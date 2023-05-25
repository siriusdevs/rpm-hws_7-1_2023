from os.path import join

CHARS_NAME = 40
CHARS_DESC = 120

# Accounts
PAGES = 'pages'
MAIN_PAGE = join(PAGES, 'index.html')
PLACES_PAGE = join(PAGES, 'places.html')
FIND_PLACE_PAGE = join(PAGES, 'find_place.html')
REQUIRED_PARAMS = ['name', 'description', 'map_points', 'map_scale']
