from rest_framework import routers
from .views import TableViewSet, TablesViewSet

router = routers.DefaultRouter()
router.register(r'village', TableViewSet)
router.register(r'villages', TablesViewSet)
