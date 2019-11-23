# moviesAPI

Simple API for fetching movies info from database. 

#### Instructions:
* clone repository
* if you don't have OMDB API key yet, go to their website (https://www.omdbapi.com/apikey.aspx) and get one - then paste it into the API_KEY field in settings.py file
* execute `docker-compose up`
* when app is built and running, execute `docker-compose exec web python manage.py migrate`
* enjoy the application!

#### Endpoints:
* `GET /movies`: will return all movies from database and their data.  
You can also:
    * filter results by providing parameters in URL, for example `/movies?genre=drama&year=2012` will return all drama movies released in 2012.  
    Avaliable filters:
        * year, 
        * min_year,
        * max_year,
        * rated,
        * genre,
        * actor,
        * director,
        * writer,
        * language,
        * country,
        * min_imdb_rating,
        * max_imdb_rating,
        * title,
        * id.
    * order results by given field.  
    Avaliable ordering fields:
        * year,
        * title,
        * imdb_rating.
* `POST /movies`: important! _title_ field in body is obligatory! That method will fetch movie data from external API, save it to database and return it to you.
* `GET /comments`: will return all comments attached to movies. There is only one way of filtering: `/comments?movie=1` will return only comments for the movie of _id_ 1.
* `POST /comments`: with obligatory _movie_ and _body_ fields in the request body, will save comment to database and return it to user.
* `GET /top?start=<start_date>&end=<end_date>`: is made for returning ranking of most commented movies in the specified date range. Both _start_ and _end_ parameters are required! Also note that valid date format is `YYYY-MM-DD`.
