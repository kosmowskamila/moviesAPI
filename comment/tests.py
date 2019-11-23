from rest_framework import status
from rest_framework.test import APITestCase

from comment.models import Comment
from movie.models import Movie


class CommentTests(APITestCase):
    """
    Tests for /comments endpoint.
    """
    def setUp(self):
        """
        Tests preparation. Filling tables with sample data.
        Three movies: Joker, Fight Club and Pulp Fiction.
        Two comments: for Joker and Fight Club.
        """
        url = '/movies'
        test_movies = [{'title': 'Joker'}, {'title': 'Fight Club'},
                       {'title': 'Pulp Fiction'}]
        for test_movie in test_movies:
            self.client.post(url, test_movie, format='json')

        Comment.objects.create(movie=Movie.objects.get(title='Joker'),
                               body='Masterpiece.')
        Comment.objects.create(movie=Movie.objects.get(title='Fight Club'),
                               body='Love that plot-twist.')

    def test_post_comment(self):
        """
        Test simple post.
        """
        url = '/comments'
        data = {'movie': Movie.objects.get(title='Joker').id, 'body': 'Awesome!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)

    def test_invalid_post_comment(self):
        """
        Test post with invalid movie ID.
        """
        url = '/comments'
        data = {'movie': Movie.objects.last().id+1, 'body': 'Awesome!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 2)

    def test_get_comments(self):
        """
        Test get of all comments.
        """
        url = '/comments'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_movie_comments(self):
        """
        Test get of comments with specified movie id.
        """
        joker_id = Movie.objects.get(title='Joker').id
        url = f'/comments?movie={joker_id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
