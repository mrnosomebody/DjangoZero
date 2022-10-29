from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,
                    password=None,
                    is_active=False,
                    is_admin=False,
                    is_superuser=False
                    ):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser
        )
        user.set_password(password)
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
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=False)  # will be activated via email confirmation
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    object = UserManager()

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

    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj=None)

    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)

    @property
    def is_staff(self):
        return self.is_admin
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField()
    rating = models.DecimalField(decimal_places=1, max_digits=2, default=0, blank=True)

    def __str__(self):
        return self.name

    def update_rating(self, company_id, val):
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
        super().save()
        self.company.update_rating(self.company.id, self.rating)


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
