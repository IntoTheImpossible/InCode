from flask_testing import TestCase
import unittest
from main import app
from steganography import KeyMixer


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
    # index route test
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to En|CO|De', response.data)
    # upload route test
    def test_upload_route(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file uploaded', response.data)
    def test_upload_route_not_select(self):
        response = self.app.post('/upload', data={"selectedOption": "some_option"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'You didn`t select option', response.data)


    # download route test   
    def test_download_route(self):
        response = self.app.post('/download/1.png')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file for downloading', response.data)
    def test_download_keys_route(self):
        response = self.app.post('/download-keys/1.png')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file for downloading', response.data)
    
    # decode and encrypt route test
    def test_decode_route(self):
        response = self.app.post('/decode')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You haven`t uploaded the image', response.data)
    def test_decode_route_get(self):
        response = self.app.get('/decode')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You haven`t uploaded the image', response.data)
    # encrypt route test
    def test_encrypt_route(self):
        response = self.app.post('/encrypt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You haven`t uploaded the image', response.data)
    def test_encrypt_route_get(self):
        response = self.app.get('/encrypt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You haven`t uploaded the image', response.data)
    # error route test
    def test_unreal_route(self):
        response = self.app.get('/unreal')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Not Found', response.data)

class KeyMixerTests(unittest.TestCase):
    def setUp(self):
        self.key = [(1, 2, 3), (4, 5, 6)]
        self.encrypted_key = [(6, 7, 8), (9, 15, 16)]
        self.encrypted_key_str = "6-7-8-9-15-16-"
        self.decrypted_key = [(1, 2, 3), (4, 5, 6)]
        self.key_str = "1-2-3-4-5-6-"

    def test_encryptor(self):
        encrypted_key = KeyMixer.encryptor(self.key)
        self.assertEqual(encrypted_key, self.encrypted_key)

    def test_decryptor(self):
        decrypted_key = KeyMixer.decryptor(self.encrypted_key)
        self.assertEqual(decrypted_key, self.decrypted_key)

    def test_keyTransformation(self):
        key_str = KeyMixer.keyTransformation(self.key)
        self.assertEqual(key_str, self.key_str)

    def test_textTransformation(self):
        key = KeyMixer.textTransformation(self.key_str)
        self.assertEqual(key, self.key)

 
if __name__ == '__main__':
    unittest.main()
