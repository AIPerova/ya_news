from django.conf import settings
import pytest

from django.urls import reverse


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('id_for_news')),
        ('news:edit', pytest.lazy_fixture('id_for_comment'))
    )
)
def test_pages_contains_form(author_client, name, args):
    """Тестирование видимости формы для разных пользователей"""
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context


def test_news_count(db, all_news, client):
    """Тестирование кол-ва отображения новостей на главной"""
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(db, all_news, admin_client):
    """Тестирование сортировки новостей"""
    response = admin_client.get(reverse('news:home'))
    object_list = response.context['object_list']
    first_news_date = object_list[0].date
    all_dates = [news.date for news in object_list]
    assert first_news_date == max(all_dates)


def test_comment_order(db, all_comments, news, admin_client):
    """Тестирование сортировки комментариев"""
    response = admin_client.get(reverse('news:detail', args=(news.id,)))
    assert 'news' in response.context
    news = response.context['news']
    comments_for_news = news.comment_set.all()
    assert comments_for_news[0].created < comments_for_news[1].created
