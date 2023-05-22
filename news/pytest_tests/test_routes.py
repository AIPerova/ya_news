from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup',)
)
def test_home_availability_for_anonymous_user(client, name, db):
    """Главная страница доступна всем"""
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_page_detail_for_anonymous_user(admin_client, id_for_news, db):
    """Страница отдельной новости доступна всем """
    url = reverse('news:detail', args=(id_for_news))
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(db, parametrized_client,
                                                name,
                                                id_for_comment,
                                                expected_status,):
    url = reverse(name, args=(id_for_comment))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment')),
    ),
)
def test_redirects(db, client, name, comment_object):
    """Тестирование переадресации анонимного пользователя"""
    login_url = reverse('users:login')
    url = reverse(name, args=(comment_object.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
