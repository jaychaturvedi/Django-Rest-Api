from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse

# automated
# new / blank db

from postings.models import UserProfile
User = get_user_model()

class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testcfeuser', email='test@test.com')
        user_obj.set_password("somerandopassword")
        user_obj.save()
        user_profile = UserProfile.objects.create(
                user=user_obj, 
                name= "Some rando title",
                address = "some more content",
                city="durgapur",
                contact = "1231231231"
                )


    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = UserProfile.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        # test the get list
        data = {}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item(self):
        # test the get list
        data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_item(self):
        # test the get list
        user_profile = UserProfile.objects.first()
        data = {}
        url = user_profile.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        # test the get list
        user_profile = UserProfile.objects.first()
        url = user_profile.get_api_url()
        data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_item_with_user(self):
        # test the get list
        user_profile = UserProfile.objects.first()
        #print(user_profile.content)
        url = user_profile.get_api_url()
        data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_post_item_with_user(self):
        # test the get list
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_ownership(self):
        # test the get list
        owner = User.objects.create(username='testuser22222')
        user_profile = UserProfile.objects.create(
                user=owner, 
                name= "Some rando title",
                address = "some more content",
                city="durgapur",
                contact = "1231231231"
                )

        user_obj            = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload             = payload_handler(user_obj)
        token_rsp           = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = user_profile.get_api_url()
        data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'testcfeuser',
            'password': 'somerandopassword'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            user_profile = UserProfile.objects.first()
            #print(user_profile.content)
            url = user_profile.get_api_url()
            data = {"name": "Some rando title", "address": "some more content","city":"durgapur","contact":"1231231231"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token) # JWT <token>
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)






# request.post(url, data, headers={"Authorization": "JWT " + <token> })