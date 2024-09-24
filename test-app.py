import unittest
import json
from app import create_app
from models import setup_db, db, Movie, Actor
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
        self.jwt_token_admin = "your_admin_jwt_token_here"
        self.jwt_token_user = "your_user_jwt_token_here"

        # Example new movie for POST requests
        self.new_movie = {
            "title": "New Movie",
            "release_date": "2024-01-01",
            "actors": [1, 2]
        }

        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            

    def test_(self):
        
        res = self.client().get('/info')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        
