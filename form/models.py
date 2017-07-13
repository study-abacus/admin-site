from django.db import models
from .conf import COURSES, CI, GENDER
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.

class Student(models.Model):

	phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

	#mendatory
	student_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=10, choices=GENDER)
	ci = models.CharField(max_length=200, choices=CI)

	#optional
	doe = models.DateField(null=True, blank=True, default=timezone.now())
	dob = models.DateField(null=True, blank=True, default=timezone.now())
	clas = models.IntegerField(blank=True, null=True)
	school = models.CharField(max_length=200, blank=True)
	adhaar = models.IntegerField(null=True, blank=True)
	father_name = models.CharField(max_length=100, blank=True)
	mobile_f = models.CharField(validators=[phone_regex], blank=True, max_length=15)
	occupation_father = models.CharField(max_length=100, blank=True)
	mother_name = models.CharField(max_length=100, blank=True)
	mobile_m = models.CharField(validators=[phone_regex], blank=True, max_length=15)
	occupation_mother = models.CharField(max_length=100, blank=True)
	annual_income = models.IntegerField(null=True, blank=True)

	def getCi(self):
		try:
			return CI[int(self.ci)-1][1]
		except:
			return self.ci

	def __str__ (self):
		return self.name

class Course(models.Model):
	student = models.ForeignKey(Student)
	course = models.CharField(max_length=2, choices=COURSES)
	level = models.IntegerField()

	def levelIncrease(self):
		self.level += 1

	def levelDecrease(self):
		self.level -= 1

	def __str__(self):
		return "%s-%d" % (self.course, self.level)

class Fee(models.Model):
	student = models.ForeignKey(Student)
	date = models.DateField(default=timezone.now())
	amount = models.IntegerField()
	remarks = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return "%d/%d, Rs.%d" % (self.date.month, self.date.year, self.amount)