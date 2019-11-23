from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError

from movie.models import Movie, Rating
from comment.models import Comment


class MoviePostTests(APITestCase):
    """
    Tests for POST request for the /movies endpoint.
    """
    def test_movie(self):
        """
        Simple post request test.
        """
        url = '/movies'
        data = {'title': 'Joker'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().title, 'Joker')

    def test_rating_create(self):
        """
        Check if rating is created when performing successful post.
        """
        url = '/movies'
        data = {'title': 'Joker'}
        _ = self.client.post(url, data, format='json')
        self.assertNotEqual(Rating.objects.count(), 0)

    def test_series(self):
        """
        Test title entry that is not a movie. Should return an error.
        """
        url = '/movies'
        response = self.client.post(url, {'title': 'Dark'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.count(), 0)

    def test_invalid_title(self):
        """
        Test non-existing movie. Should return an error.
        """
        url = '/movies'
        response = self.client.post(url, {'title': 'IHopeThisDoesntExist'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.count(), 0)

    def test_invalid_post(self):
        """
        Test with empty body. Should return an error.
        """
        url = '/movies'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.count(), 0)

    def test_post_movie_twice(self):
        """
        Test if requesting the same title twice will create two database
        entries. Should create only one.
        """
        url = '/movies'
        data = {'title': 'Joker'}
        _ = self.client.post(url, data, format='json')
        _ = self.client.post(url, data, format='json')
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().title, 'Joker')

    def test_post_movie_twice_different_title(self):
        """
        Sometimes two different queries get the same response.
        Test if in such case there are two entries created. Only one
        should be present.
        """
        url = '/movies'
        self.client.post(url, {'title': 'Avengers'}, format='json')
        self.client.post(url, {'title': 'The Avengers'}, format='json')
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().title, 'The Avengers')


class MovieGetTests(APITestCase):
    """
    Tests for GET request for the /movies endpoint.
    """
    def setUp(self):
        """
        Tests preparation. Filling movies table with sample data.
        Three movies:
        - Joker (genre: "Crime, Drama, Thriller", year: 2019),
        - Fight Club (genre: "Drama", year: 1999),
        - Pulp Fiction (genre: "Crime, Drama", year: 1994)
        """
        url = '/movies'
        test_movies = [{'title': 'Joker'}, {'title': 'Fight Club'},
                       {'title': 'Pulp Fiction'}]
        for test_movie in test_movies:
            self.client.post(url, test_movie, format='json')

    def test_get(self):
        """
        Test for returning all movies in database.
        """
        url = '/movies'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(['Joker', 'Fight Club', 'Pulp Fiction']),
                         sorted(titles))

    def test_get_genre(self):
        """
        Test filtering by genre Thriller. Should return only Joker movie.
        """
        url = '/movies?genre=thriller'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(['Joker'], titles)

    def test_get_empty_genre(self):
        """
        Test for genre that isn't present in database.
        """
        url = '/movies?genre=romance'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_newer_than(self):
        """
        Test for movies released after 2000.
        """
        url = '/movies?min_year=2000'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(['Joker'], titles)

    def test_older_than(self):
        """
        Test for movies released before 2000.
        """
        url = '/movies?max_year=2000'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(['Fight Club', 'Pulp Fiction']),
                         sorted(titles))

    def test_year_descending_order(self):
        """
        Test for order by year (descending).
        """
        url = '/movies?ordering=-year'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(['Joker', 'Fight Club', 'Pulp Fiction'], titles)

    def test_year_ascending_order(self):
        """
        Test for order by year (ascending).
        """
        url = '/movies?ordering=year'
        response = self.client.get(url)
        titles = [item['title'] for item in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(['Pulp Fiction', 'Fight Club', 'Joker'], titles)


class MovieOtherMethodsTests(APITestCase):
    def test_put(self):
        """
        Test if PUT method is allowed. Should not be allowed.
        """
        url = '/movies'
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        """
        Test if DELETE method is allowed. Should not be allowed.
        """
        url = '/movies'
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TopMoviesTests(APITestCase):
    """
    Tests for /top endpoint.
    """
    def setUp(self):
        """
        Filling database with sample data. Three movies (like in the
        example above), and four comments:
        - Joker, added 2019-11-01
        - Joker, added 2019-11-05
        - Pulp Fiction, added 2012-10-07
        - Fight Club, added 2014-05-29
        """
        url = '/movies'
        test_movies = [{'title': 'Joker'}, {'title': 'Fight Club'},
                       {'title': 'Pulp Fiction'}]
        for test_movie in test_movies:
            self.client.post(url, test_movie, format='json')
        test_comments = [
            {'movie': Movie.objects.get(title='Joker'), 'body': 'Disturbing', 'created': '2019-11-01'},
            {'movie': Movie.objects.get(title='Joker'), 'body': 'Masterpiece', 'created': '2019-11-05'},
            {'movie': Movie.objects.get(title='Pulp Fiction'), 'body': 'Tarantino is a genius', 'created': '2012-10-07'},
            {'movie': Movie.objects.get(title='Fight Club'), 'body': 'Awesome plot-twist!', 'created': '2014-05-29'},
        ]
        for test_comment in test_comments:
            comment = Comment.objects.create(movie=test_comment['movie'], body=test_comment['body'])
            comment.created = test_comment['created']
            comment.save()

    def test_big_date_range(self):
        """
        Test for date range that includes all comments.
        As result, Joker has rank 1 and Pulp Fiction and Fight club have
        both rank 2.
        """
        url = '/top?start=2000-01-01&end=2020-01-01'
        joker_id = Movie.objects.get(title='Joker').id
        response = self.client.get(url)

        self.assertEqual(response.data[0]['movie_id'], joker_id)
        self.assertEqual(response.data[0]['total_comments'], 2)
        self.assertEqual(response.data[0]['rank'], 1)

        self.assertEqual(response.data[1]['total_comments'], response.data[2]['total_comments'])
        self.assertEqual(response.data[1]['rank'], response.data[2]['rank'])

    def test_smaller_date_range(self):
        """
        Test for date range that includes one comment for Joker and one
        for Fight Club.
        As result, both Joker and Fight Club have rank 1 and Pulp Fiction
        has rank 2.
        """
        url = '/top?start=2013-01-01&end=2019-11-02'
        pulp_fiction_id = Movie.objects.get(title='Pulp Fiction').id
        response = self.client.get(url)

        self.assertEqual(response.data[2]['movie_id'], pulp_fiction_id)
        self.assertEqual(response.data[2]['total_comments'], 0)
        self.assertEqual(response.data[2]['rank'], 2)

        self.assertEqual(response.data[0]['total_comments'], response.data[1]['total_comments'])
        self.assertEqual(response.data[0]['rank'], response.data[1]['rank'])

    def test_smallest_date_range(self):
        """
        Test for date range that includes one comment for Fight Club.
        As result, Fight Club has rank 1 and Pulp Fiction and Joker have
        both rank 2.
        """
        url = '/top?start=2013-01-01&end=2015-01-01'
        fight_club_id = Movie.objects.get(title='Fight Club').id
        response = self.client.get(url)

        self.assertEqual(response.data[0]['movie_id'], fight_club_id)
        self.assertEqual(response.data[0]['total_comments'], 1)
        self.assertEqual(response.data[0]['rank'], 1)

        self.assertEqual(response.data[1]['total_comments'], response.data[2]['total_comments'])
        self.assertEqual(response.data[1]['rank'], response.data[2]['rank'])

    def test_no_date_range(self):
        """
        Test for invalid request, that doesn't have date range specified.
        """
        url = '/top'
        with self.assertRaises(ValidationError):
            self.client.get(url)

    def test_no_start_date(self):
        """
        Test for invalid request, that doesn't have start date specified.
        """
        url = '/top?end=2020-11-23'
        with self.assertRaises(ValidationError):
            self.client.get(url)

    def test_no_end_date(self):
        """
        Test for invalid request, that doesn't have end date specified.
        """
        url = '/top?start=1999-11-23'
        with self.assertRaises(ValidationError):
            self.client.get(url)

    def test_post(self):
        """
        Test if POST request is allowed. Should not be allowed.
        """
        url = '/top'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
