from django.db import models
from django.contrib.auth.models import User


# class User(User):
#     ...


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField()
    rating = models.DecimalField(decimal_places=1, max_digits=2, default=0, blank=True)

    def __str__(self):
        return self.name

    def _update_rating(self, company_id, val):
        reviews_count = len(Review.objects.filter(pk=company_id))
        self.rating = (self.rating + val) / reviews_count

    class Meta:
        verbose_name_plural = 'Companies'


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    country = models.CharField(max_length=155)
    city = models.CharField(max_length=155)
    address = models.CharField(max_length=155)  # google autocomplete may be added here
    discounts = models.TextField(blank=True, null=True)
    b_phone = models.CharField(max_length=11)  # validator needed

    def __str__(self):
        return f"{self.company.name} branch in {self.city}"

    class Meta:
        verbose_name_plural = 'Branches'


class Cuisine(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s review - {self.rating}"

    def save(self):
        self.company._update_rating(self.company.id, self.rating)
        super().save()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorites"


class CompanyCuisine(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company.name} - {self.cuisine.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'cuisine'], name='CompanyCuisine Unique')
        ]
