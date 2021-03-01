from datetime import datetime

from django.db.models import Count
from django.test import TestCase
from pytz import UTC

from db.models import User, Blog, Topic
from db.query import (
    create,
    edit_all,
    edit_u1_u2,
    delete_u1,
    unsubscribe_u2_from_blogs,
    get_topic_created_grated,
    get_topic_title_ended,
    get_user_with_limit,
    get_topic_count,
    get_avg_topic_count,
    get_blog_that_have_more_than_one_topic,
    get_topic_by_u1,
)


class TestQuery(TestCase):
    """Test query module functions"""

    def setUp(self):
        create()

    def test_create(self):
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

    def test_edit_all(self):
        edit_all()

        self.assertEqual(User.objects.filter(first_name='u1').count(), 0)
        self.assertEqual(User.objects.count(), 3)

        self.assertTrue(User.objects.get(first_name='uu1', last_name='u1'))
        self.assertTrue(User.objects.get(first_name='uu1', last_name='u2'))
        self.assertTrue(User.objects.get(first_name='uu1', last_name='u3'))

    def test_edit_u1_u2(self):
        edit_u1_u2()

        self.assertEqual(
            User.objects.filter(first_name__in=('u1', 'u2')).count(), 0
        )
        self.assertEqual(User.objects.count(), 3)

        self.assertTrue(User.objects.get(first_name='uu1', last_name='u1'))
        self.assertTrue(User.objects.get(first_name='uu1', last_name='u2'))
        self.assertTrue(User.objects.get(first_name='u3', last_name='u3'))

    def test_delete_u1(self):
        delete_u1()

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(first_name='u1').count(), 0)

    def test_unsubscribe_u2_from_blogs(self):
        unsubscribe_u2_from_blogs()

        user = User.objects.get(first_name='u2')
        self.assertEqual(
            user.subscriptions.count(), 0
        )
        self.assertNotIn(
            user,
            list(Blog.objects.get(title='blog1').subscribers.all())
        )
        self.assertNotIn(
            user,
            list(Blog.objects.get(title='blog2').subscribers.all())
        )

    def test_get_topic_created_grated(self):
        topics = get_topic_created_grated()
        for topic in topics:
            self.assertGreater(topic.created, datetime(2018, 1, 1, tzinfo=UTC))

    def test_get_topic_title_ended(self):
        self.assertTrue(get_topic_title_ended().title.endswith('content'))

    def test_get_user_with_limit(self):
        u2 = User.objects.get(id=2)
        u3 = User.objects.get(id=3)
        self.assertEqual(
            [u3, u2],
            get_user_with_limit()
        )

    def test_get_topic_count(self):
        blog1_topic_count = Topic.objects.filter(blog_id=1).count()
        blog2_topic_count = Topic.objects.filter(blog_id=2).count()
        self.assertEqual(
            [blog.topic_count for blog in get_topic_count()],
            sorted([blog1_topic_count, blog2_topic_count])
        )

    def test_get_avg_topic_count(self):
        topic_counts = Blog.objects.annotate(topic_count=Count('topic'))
        avg_topic_count = (
                sum(blog.topic_count for blog in topic_counts)
                / len(topic_counts)
        )
        self.assertEqual(get_avg_topic_count()['avg'], avg_topic_count)

    def test_get_blog_that_have_more_than_one_topic(self):
        blogs_with_topic_count = (
            Blog.objects.annotate(topic_count=Count('topic'))
        )
        self.assertEqual(
            get_blog_that_have_more_than_one_topic(),
            [blog for blog in blogs_with_topic_count if blog.topic_count > 1]
        )

    def test_get_topic_by_u1(self):
        topics_by_u1 = list(Topic.objects.filter(author__first_name='u1'))
        self.assertEqual(get_topic_by_u1(), topics_by_u1)
