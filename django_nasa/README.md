# Install

- pip install -r requirements.txt

# .env

- SECRET_KEY: your secret key for django
- IMAGE_API_TOKEN: your api token for image api. Contact to the image api administration to get it
- IMAGE_API_URL: url for image api server. Example: http://127.0.0.1:8000

# Run 
- python manage.py runserver 8001
- Go to http://127.0.0.1:8001/

# Docker for postgresql

docker run  -d --name image_api -e POSTGRES_USER=image_api -e POSTGRES_PASSWORD=change_me -e PGDATA=/postgres_data_inside_container -v ~/image_api/postgres_data:/postgres_data_inside_container  -p 38748:5432 
        postgres:15.1
