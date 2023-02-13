
from base_drf.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from mock import Mock


def test_is_admin_or_read_only():
    request = Mock()
    view = Mock()
    # Проверка правильности работы метода has_permission для случая,
    # когда метод запроса SAFE_METHODS
    request.method = 'GET'
    request.user = Mock()
    request.user.is_staff = False
    permission = IsAdminOrReadOnly()
    assert permission.has_permission(request, view) is True

    # Проверка правильности работы метода has_permission для случая,
    # когда user is staff
    request.method = 'POST'
    request.user.is_staff = True
    assert permission.has_permission(request, view) is True


def test_is_owner_or_read_only():
    request = Mock()
    view = Mock()
    obj = Mock()
    obj.user = 'user'
    request.user = 'user'
    permission = IsOwnerOrReadOnly()

    assert permission.has_object_permission(request, view, obj) is True
