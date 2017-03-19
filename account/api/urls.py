from rest_framework import routers
from .views import TableViewSet, TablesViewSet

router = routers.DefaultRouter()
router.register(r'table', TableViewSet)
router.register(r'tables', TablesViewSet)
