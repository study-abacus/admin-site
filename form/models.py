from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from form.conf import COURSES, CI, GENDER

# Create your models here.

SORTED_CI = sorted(CI, key = lambda x: (x[1]))

class Student(models.Model):

	phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

	#mendatory
	student_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=10, choices=GENDER)
	# ci = models.CharField(max_length=200, choices=SORTED_CI)
	ci = models.ForeignKey(User, on_delete = models.DO_NOTHING)

	#optional
	doe = models.DateField(null=True, blank=True, default = timezone.now)
	dob = models.DateField(null=True, blank=True, default = timezone.now)
	clas = models.IntegerField(blank=True, null=True)
	school = models.CharField(max_length=200, blank=True)
	adhaar = models.IntegerField(null=True, blank=True)
	father_name = models.CharField(max_length=100, blank=True)
	mobile_f = models.CharField(validators=[phone_regex], blank=True, max_length=15)
	occupation_father = models.CharField(max_length=100, blank=True)
	mother_name = models.CharField(max_length=100, blank=True)
	mobile_m = models.CharField(validators=[phone_regex], blank=True, max_length=15)
	occupation_mother = models.CharField(max_length=100, blank=True)
	address = models.CharField(max_length=1000, blank=True)
	annual_income = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default = True)

	def getCi(self):
		return self.ci.first_name + " " + self.ci.last_name

	def getLatestFee(self):
		return self.fee_set.order_by("-date")[0] if self.fee_set.count() > 0 else None

	def __str__ (self):
		return self.name

class Course(models.Model):
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	course = models.CharField(max_length=2, choices=COURSES)
	level = models.IntegerField()

	def levelIncrease(self):
		self.level += 1

	def levelDecrease(self):
		self.level -= 1

	def __str__(self):
		return "%s-%d" % (self.course, self.level)

class Achievement(models.Model):
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	date = models.DateField(default = timezone.now)
	score = models.FloatField()
	position = models.CharField(max_length = 100)
	remarks = models.CharField(max_length = 500)

	def __str__(self):
		return "{} - {}".format(self.student.name, self.score)

	class Meta:
		ordering = ('-date',)

class Fee(models.Model):
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	date = models.DateField(default = timezone.now)
	amount = models.IntegerField()
	remarks = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return "{}/{}, Rs.{}".format(self.date.month, self.date.year, self.amount)

	class Meta:
		ordering = ('-date',)