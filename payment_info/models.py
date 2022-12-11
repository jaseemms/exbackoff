import uuid
from django.db import models

from django.contrib.auth.models import User


class PaymentInfo(models.Model):
	"""Model to store payment processing details."""

	# Considering payment processing has three status pending, completed or failed.
	PAYMENT_STATUS_CHOICES = (
		('pending', 'Pending'),
		('completed', 'Completed'),
		('failed', 'Failed')
	)

	# Payment_id is the unique field used to identify the payment info instance.
	# Using uuid to ensure payment_id is unique across multiple instance of app and less trackable.
	payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.PROTECT) # User who trigger the payment process.
	created_at = models.DateTimeField(auto_now_add=True)
	# Datetime to identify status updated from pending to completed or failed.
	processed_at = models.DateTimeField(null=True)
	# Considering amount has not morethan 20 digits including decimal places.
	amount = models.DecimalField(max_digits=20, decimal_places=2)
	payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

	class Meta:
		verbose_name = 'Payment Info'
		verbose_name_plural = 'Payment Info'
		get_latest_by = '-created_at'
		ordering = ['-created_at']

	def __str__(self):
		# Using payment_id to uniquly identify the PaymentInfo instance.
		return self.payment_id.__str__()
