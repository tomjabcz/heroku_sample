import unittest
import json
from app import create_app
from models import setup_db, db, create_data, Movie, Actor
import os

class MovieTestCase(unittest.TestCase):
    """This class represents the movie test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        self.database_name = "test"
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            os.getenv('DB_USER', 'test'),
            os.getenv('DB_PASSWORD', 'test'),
            os.getenv('DB_HOST', 'localhost'),
            os.getenv('DB_PORT', '5432'),
            self.database_name
        )
        
        
        setup_db(self.app, self.database_path)

        # Example JWT tokens (replace these with actual valid tokens)
        self.jwt_token_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRHOXhrMVNxU3loUndyTWJfUzVLOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yMXhidnN1N3NoY2J1d2d3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmNjZTkyZTA0OGI5MWRlMDM4OTk2NGMiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE3MjcxMjU1MDksImV4cCI6MTcyNzIxMTkwOSwic2NvcGUiOiIiLCJhenAiOiJjMGMyVXUzcEdwNE1ydGdCMkpaN1ZSbW9Ed2dlMnpkMiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWxsIl19.TzvQRfLN74IlL3qB8HM6U5JdlA4tUtt16ib7hEOoEPTXvlMM_J0LQVFvpaMNxfGcpPDNvQuTPYOlxqrmF5ojHOXdhmNcZlz2jqqHasTcH2DFxdwLBj_5Sau1oLV6g9rmb1zoxD0OzaLTtAecDZ236_BkXg-stCOWXWl-leatgOGD9pZm-jQlk_5pnPyzdRJGmf5uprrVua_2s6HYyqadJG6IhpFlGuoXT7yXrnYW7KQcuc07mJ2fLgDfQtzkW7DiVwCFNM_QSv0VZancsnggWYy_6026xd-EfEHCScn3U_Th6IRrWcRzF-Aj8KcVeKIbZMrEiPda4aKCI1VJyXzScw"
        self.jwt_token_manager = "your_user_jwt_token_here"
        self.jwt_token_director = "your_user_jwt_token_here"

        # Example new movie for POST requests
        self.new_movie = {
            "title": "New Movie",
            "release_date": "2024-01-01",
            "actors": [1, 2]
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            create_data()

        
        


    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
        
            

    def test_test(self):
        """Test info endpoint - no authorization"""
        res = self.client().get('/info')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    
    def test_create_new_movie(self):
        """Test creating a new movie with valid JWT token"""
        res = self.client().post('/movies', json=self.new_movie,
                                headers={"Authorization": f"Bearer {self.jwt_token_assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])


    def test_create_movie_unauthorized(self):
        """Test that movie creation fails without JWT token"""
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
    