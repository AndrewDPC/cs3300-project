from django.test import TestCase, SimpleTestCase
from django.urls import reverse  
from django.contrib.auth.models import User, Group
from .models import LegoSet
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# Create your tests here.

#Test to see that, once user has registered, check if redirected back to login page, and once they login if it leads to homepage
class UserRegistrationLoginTest(TestCase):

    def test_register_login(self):

        #Create the group 
        self.test_group = Group.objects.create(name='member')

        #Data that user will enter for registering
        registrationData = {

            'username': 'test',
            'password1': 'test!@#$',
            'password2': 'test!@#$'
        }

        #Data for user login
        loginData = {

            'username': 'test',
            'password': 'test!@#$'
        }

        '''
        Step 1: register
        '''
        #Do registration
        response = self.client.post(reverse('register-page'), data=registrationData)
        #Check if redirected back to login page
        self.assertRedirects(response, reverse('login')) 

        '''
        Step 2: login
        '''
        #Do login
        response = self.client.post(reverse('login'), data=loginData)

        #Check if the user is redirected to the homepage after successful login
        self.assertEqual(response.status_code, 302)

#Test to see if user can log out successfully
class UserLogoutTest(TestCase):

    def test_logout(self):

        #Create a test user
        self.user = User.objects.create_user(username='test', password='test!@#$')

        #Have them logged in 
        self.client.login(username='test', password='test!@#$')

        #Have them initially at homepage
        response = self.client.get(reverse('index'))

        #Check if the user is logged in
        self.assertEqual(response.status_code, 200)

        '''
        Step 1: Log user out 
        '''
        #Log out the user
        response = self.client.get(reverse('logout'))

        '''
        Step 2: Check if user is on the success page for logging out
        '''
        #Check if page is using the logout template
        self.assertTemplateUsed(response, 'registration/logout.html')

#Test to see if logged in user will be redirected back to homepage if they try to access register link
class UserFailsafe(TestCase):

    def test_goodCatch(self):

        #Create a test user
        self.user = User.objects.create_user(username='test', password='test!@#$')

        #Have them logged in 
        self.client.login(username='test', password='test!@#$')

        #Have them initially at browse tab
        response = self.client.get(reverse('browse'))

        '''
        Step 1: Have user try to access register link while logged in
        '''
        #Get the register URL
        registerUrl = reverse('register-page')

        #Perform a GET request on the register link
        response = self.client.get(registerUrl)

        #Check if response status is redirect which is 302
        self.assertEqual(response.status_code, 302)

        #Check if user was redirected to the homepage
        self.assertRedirects(response, reverse('index'))

#Test if user can successfully create a review 
class UserCreateReviewTest(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(UserCreateReviewTest, self).setUp()
        
    def tearDown(self):
        self.selenium.quit()
        super(UserCreateReviewTest, self).tearDown()
    
    def test_createReview(self):

        #Prepare for the test

        #Create the LEGO set 
        self.legoSet = LegoSet.objects.create (

            title = 'Best Set',
            description = 'This is the set that everyone must have',
            ageRating = 10,
            setNumber = 12345,
            totalBrickCount = 5432,
            minifigureCount = 5,
            yearReleased = 2007,
            satisfactionRating = 0,
            reviewCount = 0,
            thumbnail = None,
        )

        #Create the group 
        self.test_group = Group.objects.create(name='member')

        #Make sure user is registered
        registerData = {

            'username':'testUser',
            'password1': 'test!@#$',
            'password2': 'test!@#$',

        }
        self.client.post(reverse('register-page'), data=registerData, follow=True)

        #Bring up the homepage
        self.selenium.get(self.live_server_url)
        sleep(3)

        '''
        Step 1: Log in the user
        '''
        loginLink = self.selenium.find_element(By.ID, 'login')
        loginLink.click()
        sleep(3)

        usernameField = self.selenium.find_element(By.ID, 'username')
        passwordField = self.selenium.find_element(By.ID, 'password')
        signInBtn = self.selenium.find_element(By.ID, 'signInBtn')
        usernameField.send_keys('testUser')
        passwordField.send_keys('test!@#$')
        signInBtn.click()

        sleep(3)

        '''
        Step 2: Go to the browse section
        '''
        browseLink = self.selenium.find_element(By.ID, 'browse')
        browseLink.click()
        sleep(3)

        '''
        Step 3: Go to the LEGO set 
        '''
        detailsBtn = self.selenium.find_element(By.ID, 'detailBtn')
        detailsBtn.click()
        sleep(3)

        '''
        Step 4: Create the review and enter fields
        '''
        createReviewBtn = self.selenium.find_element(By.ID, 'createBtn')
        createReviewBtn.click()
        sleep(3)

        title_input = self.selenium.find_element(By.XPATH, "//table//input[@name='title']")
        opinion_input = self.selenium.find_element(By.XPATH, "//table//textarea[@name='opinion']")
        title_input.send_keys('Very cool')
        opinion_input.send_keys('This set is very cool')
        star_to_click = self.selenium.find_element(By.XPATH, "(//span[@class='fa fa-star'])[3]")
        star_to_click.click()

        sleep(3)

        submitBtn = self.selenium.find_element(By.ID, 'submitBtn')
        submitBtn.click()
        sleep(3)

#Test if user can successfully delete a review they just created
class UserDeleteReviewTest(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(UserDeleteReviewTest, self).setUp()
        
    def tearDown(self):
        self.selenium.quit()
        super(UserDeleteReviewTest, self).tearDown()
    
    def test_deleteReview(self):

        #Prepare for the test

        #Create the LEGO set 
        self.legoSet = LegoSet.objects.create (

            #Title and description of the set 
            title = 'Best Set',
            description = 'This is the set that everyone must have',
            ageRating = 10,
            setNumber = 12345,
            totalBrickCount = 5432,
            minifigureCount = 5,
            yearReleased = 2007,
            satisfactionRating = 0,
            reviewCount = 0,
            thumbnail = None,
        )

        #Create the group 
        self.test_group = Group.objects.create(name='member')

        #Make sure user is registered
        registerData = {

            'username':'testUser',
            'password1': 'test!@#$',
            'password2': 'test!@#$',

        }
        self.client.post(reverse('register-page'), data=registerData, follow=True)

        self.selenium.get(self.live_server_url)

        '''
        Step 1: Log in the user
        '''
        loginLink = self.selenium.find_element(By.ID, 'login')
        loginLink.click()

        usernameField = self.selenium.find_element(By.ID, 'username')
        passwordField = self.selenium.find_element(By.ID, 'password')
        signInBtn = self.selenium.find_element(By.ID, 'signInBtn')
        usernameField.send_keys('testUser')
        passwordField.send_keys('test!@#$')
        signInBtn.click()

        '''
        Step 2: Go to the browse section
        '''
        browseLink = self.selenium.find_element(By.ID, 'browse')
        browseLink.click()

        '''
        Step 3: Go to the LEGO set 
        '''
        detailsBtn = self.selenium.find_element(By.ID, 'detailBtn')
        detailsBtn.click()

        '''
        Step 4: Create the review and enter fields
        '''
        createReviewBtn = self.selenium.find_element(By.ID, 'createBtn')
        createReviewBtn.click()

        title_input = self.selenium.find_element(By.XPATH, "//table//input[@name='title']")
        opinion_input = self.selenium.find_element(By.XPATH, "//table//textarea[@name='opinion']")
        title_input.send_keys('Very cool')
        opinion_input.send_keys('This set is very cool')
        star_to_click = self.selenium.find_element(By.XPATH, "(//span[@class='fa fa-star'])[4]")
        star_to_click.click()


        submitBtn = self.selenium.find_element(By.ID, 'submitBtn')
        submitBtn.click()

        '''
        Step 5: Delete the review that was just created
        '''
        sleep(2)
        self.selenium.execute_script("window.scrollBy(0, window.innerHeight / 2);") #Force scroll so that element can be seen
        sleep(1)
        deleteBtn = self.selenium.find_element(By.ID, 'deleteBtn')
        deleteBtn.click()
        sleep(3)

        '''
        Step 6: Delete the review using button on modal
        '''
        deleteBtnModal = self.selenium.find_element(By.ID, 'deleteModalBtn')
        deleteBtnModal.click()
        sleep(3)

      
        









       












     

