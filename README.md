# Mars Project

Mars Project is a web application that provides a platform for professional relocator to Mars. It allows users to authenticate, register, view rover images from NASA's API, and maintain a history of image requests.


## Features

- User authentication and registration
- Viewing rover images from NASA's API based on Sol (Martian day)
- Maintaining a history of image requests
- Secure session management using cookies


## Installation

1. Clone the repository:
<pre>
    git clone https://github.com/Nirtkor/rpm-hws_7-1_2023 -b orehov
</pre>

2. Set up the PostgreSQL database:
- Start a PostgreSQL container with the following command:
  ```
  docker run -d \
  --name mars_project \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e PGDATA=/postgres_data_inside_container \
  -v /path/to/host/postgres_data:/postgres_data_inside_container \
  -p 38746:5432 \
  postgres:15.1
  ```
  Replace `/path/to/host/postgres_data` with the path to the directory where you want to store the PostgreSQL data on your host machine.

3. Configure environment variables:
- Create a `.env` file in the project root directory.
- Add the following environment variables to the `.env` file:
  ```
  PG_DBNAME=postgres
  PG_HOST=127.0.0.1
  PG_PORT=38746
  PG_USER=admin
  PG_PASSWORD=admin
  ```

4. Run the application:

  ```
  python3 main.py
  ```

5. Open your web browser and visit `http://localhost:8000` to access the Mars Project application.

## Usage

- Home Page (`/`): The main page of the application where users can view information about Mars and access authentication and registration forms.
- Login Page (`/login`): Users can log in with their credentials to access the `/info` page.
- Registration Page (`/register`): New users can register their account by providing a username, password, and Sol (Martian day) value.
- Info Page (`/info`): Authenticated users can view the latest rover image based on the specified Sol value.
- History Page (`/history`): Users can view the history of image requests stored in the database.

## Contributing

Contributions to Mars Project are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.