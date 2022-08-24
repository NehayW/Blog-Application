from django.test import TestCase
from account.forms import SignupForm, UpdateProfileForm


class RegisterFormTestFields(TestCase):
    def test_form_first_name_field(self):
        form =  SignupForm()
        self.assertTrue(form.fields['first_name'].label=='First name')

    def test_form_last_name_field(self):
        form = SignupForm()
        self.assertTrue(form.fields['last_name'].label=='Last name')
    
    def test_form_email_field(self):
        form = SignupForm()
        print(form.fields['email'].label)
        self.assertTrue(form.fields['email'].label=='Email address')

    def test_form_image_field(self):
        form = SignupForm()
        self.assertTrue(form.fields['profile_image'].label=="Profile image")


class RegisterFormTest2(TestCase):
    def test_registration(self):
        form_data = {'email':'data@gmail.com', 
                     'first_name':'test', 
                     'password1':'mohit@123',
                     'password2':'mohit@123'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

class UpdateProfileTest(TestCase):
    def test_update_profile(self):
        form_data = {'first_name':'test2',
                     'last_name':'last_name_test',
                     }
        form = UpdateProfileForm(data=form_data)
        self.assertTrue(form.is_valid())