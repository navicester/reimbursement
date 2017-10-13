
from django.db import models

class InvoiceImage(models.Model):
	image = models.ImageField(upload_to='img/upload')	

	def __unicode__(self):
		return self.id