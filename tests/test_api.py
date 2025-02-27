# import unittest
# from app import create_app, db
# from flask import json
# from flask_jwt_extended import create_access_token

# class TestAPI(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(test_cfg=True)
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         self.client = self.app.test_client()
        
#         # Создаем таблицы
#         db.create_all()
        
#         # Регистрируем тестового пользователя
#         self.client.post('/auth/register', 
#                         data=json.dumps({"email": "test@example.com", "password": "pass123"}),
#                         content_type='application/json')
#         self.token = create_access_token(identity="1")

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     # def test_register_success(self):
#     #     response = self.client.post('/auth/register', 
#     #                               data=json.dumps({"email": "new@example.com", "password": "pass456"}),
#     #                               content_type='application/json')
#     #     self.assertEqual(response.status_code, 201)

#     # def test_register_existing_email(self):
#     #     response = self.client.post('/auth/register', 
#     #                               data=json.dumps({"email": "test@example.com", "password": "pass123"}),
#     #                               content_type='application/json')
#     #     self.assertEqual(response.status_code, 400)

#     # def test_login_success(self):
#     #     response = self.client.post('/auth/login', 
#     #                               data=json.dumps({"email": "test@example.com", "password": "pass123"}),
#     #                               content_type='application/json')
#     #     self.assertEqual(response.status_code, 200)

#     # def test_login_wrong_password(self):
#     #     response = self.client.post('/auth/login', 
#     #                               data=json.dumps({"email": "test@example.com", "password": "wrongpass"}),
#     #                               content_type='application/json')
#     #     self.assertEqual(response.status_code, 401)

#     # def test_create_referral_code_success(self):
#     #     response = self.client.post('/referral/code', 
#     #                               data=json.dumps({"expires_at": "2025-12-31"}),
#     #                               headers={"Authorization": f"Bearer {self.token}", 
#     #                                       "Content-Type": "application/json"})
#     #     self.assertEqual(response.status_code, 201)

#     # def test_delete_referral_code_success(self):
#     #     self.client.post('/referral/code', 
#     #                     data=json.dumps({"expires_at": "2025-12-31"}),
#     #                     headers={"Authorization": f"Bearer {self.token}", 
#     #                             "Content-Type": "application/json"})
#     #     response = self.client.delete('/referral/code', 
#     #                                 headers={"Authorization": f"Bearer {self.token}"})
#     #     self.assertEqual(response.status_code, 200)

#     # def test_get_code_by_email_success(self):
#     #     self.client.post('/referral/code', 
#     #                     data=json.dumps({"email": "test@example.com"}),
#     #                     headers={"Content-Type": "application/json"})
#     #     response = self.client.get('/referral/code/by-email', data=data)
#     #     self.assertEqual(response.status_code, 200)

#     # def test_get_referrals_success(self):
#     #     response = self.client.get('/referral/referrals', 
#     #                              headers={"Authorization": f"Bearer {self.token}"})
#     #     self.assertEqual(response.status_code, 200)
