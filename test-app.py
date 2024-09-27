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

        
        self.jwt_token_expired = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRHOXhrMVNxU3loUndyTWJfUzVLOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yMXhidnN1N3NoY2J1d2d3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmNjZTkyZTA0OGI5MWRlMDM4OTk2NGMiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE3MjcxMjU1MDksImV4cCI6MTcyNzIxMTkwOSwic2NvcGUiOiIiLCJhenAiOiJjMGMyVXUzcEdwNE1ydGdCMkpaN1ZSbW9Ed2dlMnpkMiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWxsIl19.TzvQRfLN74IlL3qB8HM6U5JdlA4tUtt16ib7hEOoEPTXvlMM_J0LQVFvpaMNxfGcpPDNvQuTPYOlxqrmF5ojHOXdhmNcZlz2jqqHasTcH2DFxdwLBj_5Sau1oLV6g9rmb1zoxD0OzaLTtAecDZ236_BkXg-stCOWXWl-leatgOGD9pZm-jQlk_5pnPyzdRJGmf5uprrVua_2s6HYyqadJG6IhpFlGuoXT7yXrnYW7KQcuc07mJ2fLgDfQtzkW7DiVwCFNM_QSv0VZancsnggWYy_6026xd-EfEHCScn3U_Th6IRrWcRzF-Aj8KcVeKIbZMrEiPda4aKCI1VJyXzScw"
        self.jwt_token_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRHOXhrMVNxU3loUndyTWJfUzVLOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yMXhidnN1N3NoY2J1d2d3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmNjZTkyZTA0OGI5MWRlMDM4OTk2NGMiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE3Mjc0NjQ5NzUsImV4cCI6MTcyNzU1MTM3NSwic2NvcGUiOiIiLCJhenAiOiJjMGMyVXUzcEdwNE1ydGdCMkpaN1ZSbW9Ed2dlMnpkMiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWxsIl19.WXQwoZp_S5AkE2TMek7SNklLZwCSNUd32qKqgaIE_5KLe5qYemyM6oyqcwtNXiplPvI_0pwlv1Jpu8p0qPFHjxq2biQEep4RnUGkHNnJ5ic0-V8AGyIiC2NKlvnO3i2Wkwn-YFPE-LKwAs70LxReG4U9hZNs5bPJ23JegjY5GeNvevBjMxCAaG_jVwVkeldPtzh-0q9pTPW6yqo54jOFTdNGli4d35Du3C-_iXDdjl1lEoyx7zHUHp3KUQ70lz08PrpqNUK9SK_AahQUL-DBM3c1jPvIi0SXgoM6FAWGuZ7NXJogCrbf6wY6ZF4iO6s2GwbDCkQkyaEKhuAFrvFdDg"
        self.jwt_token_manager = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRHOXhrMVNxU3loUndyTWJfUzVLOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yMXhidnN1N3NoY2J1d2d3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmNjZTkyZTA0OGI5MWRlMDM4OTk2NGMiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE3Mjc0NjQ4NzksImV4cCI6MTcyNzU1MTI3OSwic2NvcGUiOiIiLCJhenAiOiJjMGMyVXUzcEdwNE1ydGdCMkpaN1ZSbW9Ed2dlMnpkMiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZS1kZWxldGU6YWN0b3IiLCJyZWFkOmFsbCIsInVwZGF0ZTphbGwiXX0.XrRQ22SHdSe_1xCdtrxVspDS_Db_ft_IB2Ns38al2uJI6yPjQcqDtSWbU4gwkv52kscGR2m5h76Sne7K040t4-CvlNxs1f7MqY7pUwGgFh49bn9RZu5IHNRG6yqIoAyaUoKL4XD_TGtXoQZyR5XAPWDcVv6I7qBOFMqdlp1mWBpmQE6E7Y1YPDygm_EsneCY6tQ27rKF3ZRWoojiXhGL_BLYk90qLIUSMwLOyFJQ0ub_T-sWs3g3FX19biraXw6Lk_zrA3trnUyB_n2JwkzPO1Xn4Scjgt__Fqbqkqn4nj0vWe5D-x38zO_E4W4FPNF8WN3yCkZR475cdFcrZ_6rRQ"
        self.jwt_token_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRHOXhrMVNxU3loUndyTWJfUzVLOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yMXhidnN1N3NoY2J1d2d3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmNjZTkyZTA0OGI5MWRlMDM4OTk2NGMiLCJhdWQiOiJjb2ZmZWUiLCJpYXQiOjE3Mjc0NjQzMzIsImV4cCI6MTcyNzU1MDczMiwic2NvcGUiOiIiLCJhenAiOiJjMGMyVXUzcEdwNE1ydGdCMkpaN1ZSbW9Ed2dlMnpkMiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZS1kZWxldGU6YWN0b3IiLCJjcmVhdGUtZGVsZXRlOm1vdmllIiwicmVhZDphbGwiLCJ1cGRhdGU6YWxsIl19.IUQvMfneXFDgRL4DGXPrgsKiFkXEFMZMFMjW3FY0iYlVB3TFE706vI_7gQ5hnOqvriWTrSJRGHF71H54p65GrxXleZKPXyMCoHOHQm2lQ8pm5h6ypG25zBYhUpsHfPfOFNqAdr2_qrBLz8OSJFRXXFkxTz1ZYQ412hUaMOiyNkaFJdfPShk6ulDIsfQlO_dHtcG9JlJdnj7gd307HgTcGxfL2fudOCCJh9TurgSXYzIqAqKkQ9DFqD5Lfybc1PYebEw0DqH7-YoFLAeTef7XJfhIuOKWQ-SydksU0J6EN8OSJCfaa6Z0sF8f_AghiuK3nYvvd5DPFS29Eemg6olcJw"

        # new movie for POST requests
        self.new_movie = {
            "title": "New Movie",
            "release_date": "2024-01-01",
            "actors": [1, 2]
        }

        # new actor for POST requests
        self.new_actor = {
            "name": "New Actor",
            "age": 35,
            "gender": "male"
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            create_data()
     
    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()

        
    def test_create_new_movie(self):
        """Test creating a new movie with valid JWT token"""
        res = self.client().post('/movies', json=self.new_movie,
                                headers={"Authorization": f"Bearer {self.jwt_token_director}"})
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
    
    
    def test_get_all_movies(self):
        """Test fetching all movies"""
        res = self.client().get('/movies', headers={"Authorization": f"Bearer {self.jwt_token_assistant}"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])

    def test_get_all_actors(self):
        """Test fetching all actors"""
        res = self.client().get('/actors', headers={"Authorization": f"Bearer {self.jwt_token_assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    
    def test_create_new_movie(self):
        """Test creating a new movie with valid JWT token"""
        res = self.client().post('/movies', json=self.new_movie,
                                headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

  
    def test_create_new_actor(self):
        """Test creating a new actor with valid JWT token"""
        res = self.client().post('/actors', json=self.new_actor,
                                headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    
    def test_update_movie(self):
        """Test updating an existing movie"""
        updated_data = {
            "title": "Updated Movie Title",
            "release_date": "2024-05-05"
        }
        res = self.client().patch('/movies/1', json=updated_data,
                                  headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie'], "Updated Movie Title")

    
    def test_update_actor(self):
        """Test updating an existing actor"""
        updated_data = {
            "name": "Updated Actor Name",
            "age": 40
        }
        res = self.client().patch('/actors/1', json=updated_data,
                                  headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], "Updated Actor Name")

    
    def test_delete_movie(self):
        """Test deleting a movie"""
        res = self.client().delete('/movies/1', headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

    
    def test_delete_actor(self):
        """Test deleting an actor"""
        res = self.client().delete('/actors/1', headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)


    def test_get_movies_no_auth(self):
        """Test fetching movies without authorization token"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_get_non_existent_movie(self):
        """Test fetching a movie that does not exist"""
        res = self.client().get('/movies/9999', headers={"Authorization": f"Bearer {self.jwt_token_assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        


    def test_create_movie_no_auth(self):
        """Test creating a movie without authorization"""
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_create_movie_invalid_data(self):
        """Test creating a movie with invalid data"""
        invalid_movie = {
            "title": "",  # Empty title should fail
            "release_date": "invalid-date"  # Invalid date format
        }
        res = self.client().post('/movies', json=invalid_movie,
                                 headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        


    def test_update_movie_no_auth(self):
        """Test updating a movie without authorization"""
        updated_data = {
            "title": "Updated Movie Title"
        }
        res = self.client().patch('/movies/1', json=updated_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_update_non_existent_movie(self):
        """Test updating a non-existent movie"""
        updated_data = {
            "title": "Updated Movie Title"
        }
        res = self.client().patch('/movies/9999', json=updated_data,
                                  headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        


    def test_delete_movie_no_auth(self):
        """Test deleting a movie without authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_delete_non_existent_movie(self):
        """Test deleting a non-existent movie"""
        res = self.client().delete('/movies/9999',
                                   headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        


    def test_create_actor_no_auth(self):
        """Test creating an actor without authorization"""
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_update_non_existent_actor(self):
        """Test updating a non-existent actor"""
        updated_data = {
            "name": "Updated Actor Name"
        }
        res = self.client().patch('/actors/9999', json=updated_data,
                                  headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        


    def test_delete_actor_no_auth(self):
        """Test deleting an actor without authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_delete_non_existent_actor(self):
        """Test deleting a non-existent actor"""
        res = self.client().delete('/actors/9999',
                                   headers={"Authorization": f"Bearer {self.jwt_token_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        

    def test_create_movie_with_expired_token(self):
        """Test creating a movie with expired JWT token"""
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": f"Bearer {self.jwt_token_expired}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        
    