from django.db import models
from django.utils import timezone

# Create your models here.
class Journal_Entry(models.Model):
	title = models.CharField(max_length=1024)
	details = models.TextField()
	s3_path = models.CharField(max_length=256, blank=True)
	tone = models.CharField(max_length=16, blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	last_updated_date = models.DateTimeField(blank=True, null=True)
	uid = models.CharField(max_length=96)

	def __str__(self):
		return self.uid