from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, username, firstName, lastName, email, address, phone, date_of_birth, password=None):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username = username,
            firstName = firstName,
            lastName = lastName,
            email=self.normalize_email(email),
            address = address,
            phone = phone,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, firstName, lastName, email, address, phone, date_of_birth, password=None):
        user = self.create_user(
            username=username,
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            address=address,
            phone=phone,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)

    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=200)

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    address = models.TextField()
    phone = models.CharField(max_length=15)

    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['firstName', 'lastName', 'email', 'address', 'phone', 'date_of_birth']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin