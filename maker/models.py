from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name,
            password='',
            is_active=False,
            is_admin=False,
            is_superuser=False
    ):
        password_invalid = validate_password(password, user=User)
        if password_invalid:
            return password_invalid
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser
        )
        user.set_password(password)
        #  using tells which database to use. self._db is default db from settings
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_admin=True,
            is_superuser=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=False)  # will be activated via email/phone confirmation
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name}'

    def __str__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_admin


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    email = models.EmailField()
    # this field is not necessary, but I suppose that it is better to save rating
    # and just get it rather than counting it every time it's needed
    rating = models.DecimalField(
        decimal_places=1,
        max_digits=2,
        default=0,
        blank=True
    )

    def __str__(self):
        return self.name

    def update_rating(self, val: int) -> None:
        reviews_quantity = Review.objects.filter(company=self.id).count()
        self.rating = (self.rating + val) / reviews_quantity
        self.save()

    class Meta:
        verbose_name_plural = 'Companies'


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    country = models.CharField(max_length=155)
    city = models.CharField(max_length=155)
    address = models.CharField(max_length=155)  # google autocomplete may be added here
    discounts = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    image = models.ImageField(
        upload_to='uploads/images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.company.name} branch in {self.city}"

    class Meta:
        verbose_name_plural = 'Branches'


class Cuisine(models.Model):
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.email}'s review - {self.rating}"

    # maybe it's better to move this logic to views
    def save(self):
        with transaction.atomic():
            super().save()  # do it in transaction
            self.company.update_rating(self.rating)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company'], name='UserCompany Unique')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.company.name}"


class CompanyCuisine(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company.name} - {self.cuisine.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'cuisine'], name='CompanyCuisine Unique')
        ]
