from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PaymentInfo
from .serializers import PaymentInfoSerializer
from .tasks import check_payment_status 


class PaymentInfoViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
						viewsets.GenericViewSet):
	"""
	GenericViewsSet for create, list, retrive payment info of autheticated user.

	By default submitted payment status is pending, using celery backgroud task 
	to updated status using external API endpoint.
	"""
	serializer_class = PaymentInfoSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		# Restricting access of other users payment details.
		return PaymentInfo.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		instance = serializer.save(user=self.request.user)

		# Triggering external api call to update payment status.
		check_payment_status.delay(instance.payment_id)


