from datetime import datetime

from pytz import UTC

from db.models import User, Blog, Topic


def create():
    u1 = User.objects.create(first_name='u1', last_name='u1')
    u2 = User.objects.create(first_name='u2', last_name='u2')
    u3 = User.objects.create(first_name='u3', last_name='u3')
    blog1 = Blog.objects.create(title='blog1', author=u1)
    blog2 = Blog.objects.create(title='blog2', author=u1)

    blog1.subscribers = [u1, u2]
    blog1.save()
    blog2.subscribers = [u2]
    blog2.save()

    topic1 = Topic.objects.create(title='topic1', blog=blog1, author=u1)
    topic2 = Topic.objects.create(title='topic2_content',
                                  blog=blog1,
                                  author=u3,
                                  created=datetime(2017, 1, 1, tzinfo=UTC))

    topic1.likes = [u1, u2, u3]
    topic1.save()


def edit_all():
    pass


def edit_u1_u2():
    pass


def delete_u1():
    pass


def unsubscribe_u2_from_blogs():
    pass


def get_topic_created_grated():
    pass


def get_topic_title_ended():
    pass


def get_user_with_limit():
    pass


def get_topic_count():
    pass


def get_avg_topic_count():
    pass


def get_blog_that_have_more_than_one_topic():
    pass


def get_topic_by_u1():
    pass


def get_user_that_dont_have_blog():
    pass


def get_topic_that_like_all_users():
    pass


def get_topic_that_dont_have_like():
    pass
