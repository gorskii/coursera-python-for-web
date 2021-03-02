from datetime import datetime

from django.db.models import Count, Avg
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
    """Change first_name to 'uu1' for all users"""
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    """Change first_name to 'uu1' for users
    who have first_name 'u1' or 'u2'"""
    User.objects.filter(first_name__in=('u1', 'u2')).update(first_name='uu1')


def delete_u1():
    """Delete user with first_name 'u1'"""
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    """Unsubscribe user with first_name 'u2' from blogs"""
    user = User.objects.get(first_name='u2')
    user.subscriptions = []
    user.save()


def get_topic_created_grated():
    """Return topics that have creation date greater than 2018-01-01"""
    return list(
        Topic.objects.filter(created__gt=datetime(2018, 1, 1, tzinfo=UTC))
    )


def get_topic_title_ended():
    """Return a topic whose title ends with 'content'"""
    return Topic.objects.get(title__endswith='content')


def get_user_with_limit():
    """Sort users in reverse order by id and return the first two"""
    return list(User.objects.order_by('-id')[:2])


def get_topic_count():
    """Return sorted topic counts for each blog"""
    return list(
        Blog.objects
            .annotate(topic_count=Count('topic'))
            .order_by('topic_count')
    )


def get_avg_topic_count():
    """Return average topic count for blog"""
    return (Blog.objects
            .annotate(topic_count=Count('topic'))
            .aggregate(avg=Avg('topic_count')))


def get_blog_that_have_more_than_one_topic():
    """Return blogs that have more than one topic"""
    return list(
        Blog.objects
            .annotate(topic_count=Count('topic'))
            .filter(topic_count__gt=1)
    )


def get_topic_by_u1():
    """Return topics created by user with first_name u1"""
    return list(Topic.objects.filter(author__first_name='u1'))


def get_user_that_dont_have_blog():
    """Return users that don't have any blogs, sorted by id"""
    return list(User.objects.filter(blog=None).order_by('id'))


def get_topic_that_like_all_users():
    """Return topics that all users liked"""
    return list(Topic.objects.filter(likes=User.objects.all()))


def get_topic_that_dont_have_like():
    pass
