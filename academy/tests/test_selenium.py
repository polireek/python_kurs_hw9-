import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.webdriver import WebDriver

from academy.models import Student, Lecturer


class SeleniumTest(StaticLiveServerTestCase):

    NUMBER_OF_STUDENTS = 20
    NUMBER_OF_TEACHER = 30

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    def setUp(self) -> None:
        self.user_admin = User.objects.create_user(username='testuser', password='12345')
        self.user = User.objects.create(first_name='John', last_name='Doe', email='name@domain.com')
        self._create_students(self.NUMBER_OF_STUDENTS)
        self._create_teacher(self.NUMBER_OF_TEACHER)

    def _create_students(self, num):
        for article_num in range(num):
            Student.objects.create(
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                email=self.user.email
            )

    def _create_teacher(self, num):
        for article_num in range(num):
            Lecturer.objects.create(
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                email=self.user.email
            )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_unsuccessful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('aaaaaaaaaa')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('aaaaaaaaaa')

        submit_btn = self.selenium.find_element_by_id('submit_login')
        submit_btn.submit()

        error = self.selenium.find_element_by_id('error_msg')
        expected_error = "Your username and password didn't match. Please try again."
        time.sleep(3)  # Fix ConnectionResetError i dont know why 3 but its work
        self.assertEqual(error.text, expected_error)

    def test_successful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('testuser')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('12345')

        submit_btn = self.selenium.find_element_by_id('submit_login')
        submit_btn.submit()

        username = self.selenium.find_element_by_id('username')
        time.sleep(3)  # Fix ConnectionResetError i dont know why 3 but its work
        self.assertEqual(username.text, self.user_admin.username)

    def test_sign_up(self):
        self.selenium.get(self.live_server_url)

        sign_up_btn = self.selenium.find_element_by_id('sign_up')
        sign_up_btn.click()

        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('a'*10 + '@mail.com')

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('a'*10)

        password_input = self.selenium.find_element_by_name('password1')
        password_input.send_keys('b'*10)

        password_input = self.selenium.find_element_by_name('password2')
        password_input.send_keys('b'*10)

        submit_btn = self.selenium.find_element_by_tag_name('button')
        submit_btn.submit()

        notification = self.selenium.find_element_by_id('notification')
        expected_notification = 'Please confirm your email address to complete the ' \
                                'registration.'

        time.sleep(3)

        self.assertEqual(notification.text, expected_notification)

    def test_check_pagination_students(self):
        self.selenium.get(self.live_server_url)

        students_url = self.selenium.find_element_by_id('students')
        students_url.click()

        students_url = self.selenium.find_element_by_id('get_students')
        students_url.click()

        pagination = self.selenium.find_element_by_class_name('pagination')
        self.assertTrue(bool(pagination))

    def test_check_pagination_teacher(self):
        self.selenium.get(self.live_server_url)

        students_url = self.selenium.find_element_by_id('teachers')
        students_url.click()

        students_url = self.selenium.find_element_by_id('get_teachers')
        students_url.click()

        pagination = self.selenium.find_element_by_class_name('pagination')
        self.assertTrue(bool(pagination))

    def test_exchange_rate_table_on_index_page(self):
        self.selenium.get(self.live_server_url)

        table = self.selenium.find_element_by_id('kurs')

        self.assertTrue(bool(table))
