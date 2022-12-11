from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'payments', views.PaymentInfoViewSet, basename='payment')

urlpatterns = router.urls
