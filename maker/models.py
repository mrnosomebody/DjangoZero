from django.db import models


class User(models.Model):
    ...


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField()
    cuisine = models.ForeignKey('Cuisine', on_delete=models.CASCADE)
    rating = models.DecimalField()


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    country = models.CharField(max_length=155)
    city = models.CharField(max_length=155)
    address = models.CharField(max_length=155)  # google autocomplete may be added here
    discounts = models.TextField()
    b_phone = models.CharField(max_length=11)  # validator needed


class Cuisine(models.Model):
    name = models.CharField(max_length=55)


class Review(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.IntegerField()


class Favorite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

