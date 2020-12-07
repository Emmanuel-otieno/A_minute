from app.models import Comment,User,Pitch
from app import db
import unittest

class PitchTest(unittest.TestCase):
    def setUp(self):
        self.user_Emmanuel = User(username = 'Emmanuel',password = '0725939687', email = 'sakoemmanuel4@gmail.com')
        self.new_pitch = Pitch(id=1,pitch_title='Welcome',pitch_content='Welcome Home',category="promotion",user = self.user_Emmanuel,likes=0,dislikes=0)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.pitch_title,'Welcome')
        self.assertEquals(self.new_pitch.pitch_content,'Welcome Home')
        self.assertEquals(self.new_pitch.category,"promotion")
        self.assertEquals(self.new_pitch.user,self.user_Emmanuel)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        my_pitch = Pitch.get_pitch(1)
        self.assertTrue(my_pitch is not None)
