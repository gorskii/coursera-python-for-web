from datetime import datetime

from django.test import TestCase
from pytz import UTC

from db.models import User, Blog, Topic
from db.query import create


class TestQuery(TestCase):
    """Test query module functions"""

    def test_create(self):
        create()
        u1 = User.objects.get(first_name='u1', last_name='u1')
        self.assertTrue(u1)
        u2 = User.objects.get(first_name='u2', last_name='u2')
        self.assertTrue(u2)
        u3 = User.objects.get(first_name='u3', last_name='u3')
        self.assertTrue(u3)

        blog1 = Blog.objects.get(title='blog1')
        self.assertTrue(blog1)
        self.assertTrue(Blog.objects.get(title='blog2'))

        self.assertEqual(
            [u1, u2],
            list(Blog.objects.get(title='blog1').subscribers.all())
        )
        self.assertEqual(
            [u2],
            list(Blog.objects.get(title='blog2').subscribers.all())
        )

        self.assertTrue(Topic.objects.get(title='topic1'))
        self.assertTrue(Topic.objects.get(title='topic2_content',
                                          blog=blog1,
                                          author=u3,
                                          created=datetime(2017, 1, 1,
                                                           tzinfo=UTC)))
        self.assertEqual(
            [u1, u2, u3],
            list(Topic.objects.get(title='topic1').likes.all())
        )
