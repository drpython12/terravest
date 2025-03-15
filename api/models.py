from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending the default Django AbstractUser.
    """
    username = None  # Remove the username field
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    preferences_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country', 'date_of_birth']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        """
        Return a string representation of the user, using the email.
        """
        return self.email


class PortfolioStock(models.Model):
    """
    Model representing a stock in a user's portfolio.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    shares = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_bought_at = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the portfolio stock.
        """
        return f"{self.symbol} - {self.user.email}"


class UserPreferences(models.Model):
    """
    Model to store user preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    investment_type = models.CharField(max_length=50, choices=[
        ('stocks', 'Stocks'),
        ('bonds', 'Bonds'),
        ('real_estate', 'Real Estate'),
        ('crypto', 'Cryptocurrency'),
    ])
    risk_level = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    investment_strategy = models.CharField(max_length=50, choices=[
        ('impact_investing', 'Impact Investing'),
        ('esg_integration', 'ESG Integration'),
        ('ethical_screening', 'Ethical Screening'),
        ('traditional_esg', 'Traditional Investing with ESG Consideration'),
    ])
    esg_factors = models.JSONField(default=list)  # To store multiple ESG factors
    industry_preferences = models.JSONField(default=list, blank=True)  # Optional field
    exclusions = models.JSONField(default=list, blank=True)  # Optional field
    sentiment_analysis = models.CharField(max_length=10, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
    ])
    transparency_level = models.CharField(max_length=20, choices=[
        ('simple_summary', 'Simple Summary'),
        ('detailed_breakdown', 'Detailed Breakdown'),
    ])

    def __str__(self):
        """
        Return a string representation of the user's preferences.
        """
        return f"Preferences for {self.user.email}"