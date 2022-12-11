from rest_framework import serializers

from .models import PaymentInfo


class PaymentInfoSerializer(serializers.ModelSerializer):
	"""Serializer to create and retrive payments for an authenticated user.
	"""
	class Meta:
		model = PaymentInfo
		exclude = ['user']
		# User can only submit amount details when creating an entry, all other fields are read-only.
		read_only_fields = ['processed_at', 'payment_status']
