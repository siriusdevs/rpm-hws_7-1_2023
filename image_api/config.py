"""Some constants for image api."""
NASA_IMAGE = "https://api.nasa.gov/planetary/apod?api_key={api_key}&{parameters}"
MARS_IMAGE = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key={api_key}&{parameters}"
FILES_DIR = "files/{user}/{file_name}"

SQL_TOKEN = "select token from token {parameters}"
SQL_INSERT_USER_IMAGE = "insert into user_image (user_name, title, explanation, date) values (%s, %s, %s, ""%s) " \
                        "returning id"

SQL_UPDATE_IMAGE = "update user_image set {request} {parameters}"

SQL_SELECT_USER_IMAGE = "select {request} from user_image {parameters}"
SQL_DELETE = 'DELETE FROM user_image  {parameters}'
