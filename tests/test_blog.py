import unittest
from app.models import Blog 
from app import db

class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Blog class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_blog = Blog(title='Hello world',content='My first webpage')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))

