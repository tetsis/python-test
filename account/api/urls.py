from rest_framework import routers
from .views import TableViewSet

router = routers.DefaultRouter()
router.register(r'tables', TableViewSet)
