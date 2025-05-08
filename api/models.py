from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending the default Django AbstractUser.
    """
    username = None
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    preferences_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
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
    symbol = models.CharField(max_length=10)  # Ticker
    company_name = models.CharField(max_length=100)  # New field for company name
    shares = models.PositiveIntegerField()
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_bought_at = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the portfolio stock.
        """
        return f"{self.company_name} ({self.symbol}) - {self.user.email}"


class UserPreferences(models.Model):
    """
    Model to store user preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
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

    def to_dict(self):
        """
        Convert the UserPreferences instance to a dictionary.
        """
        return {
            "risk_level": self.risk_level,
            "investment_strategy": self.investment_strategy,
            "esg_factors": self.esg_factors,
            "industry_preferences": self.industry_preferences,
            "exclusions": self.exclusions,
            "sentiment_analysis": self.sentiment_analysis,
            "transparency_level": self.transparency_level,
        }

    def update_from_dict(self, data):
        """
        Update the UserPreferences instance with data from a dictionary.
        """
        self.risk_level = data.get('riskLevel', self.risk_level)
        self.investment_strategy = data.get('investmentStrategy', self.investment_strategy)
        self.esg_factors = data.get('esgFactors', self.esg_factors)
        self.industry_preferences = data.get('industryPreferences', self.industry_preferences)
        self.exclusions = data.get('exclusions', self.exclusions)
        self.sentiment_analysis = data.get('sentimentAnalysis', self.sentiment_analysis)
        self.transparency_level = data.get('transparencyLevel', self.transparency_level)


class ESGCompany(models.Model):
    orgperm_id = models.BigIntegerField(unique=True)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    isin = models.CharField(max_length=20, blank=True)
    siccode = models.CharField(max_length=10, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ticker']),
            models.Index(fields=['orgperm_id']),
        ]

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class ESGMetric(models.Model):
    company = models.ForeignKey(ESGCompany, related_name='metrics', on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    fieldid = models.PositiveIntegerField()
    hierarchy = models.CharField(max_length=50)
    pillar = models.CharField(max_length=50)
    fieldname = models.CharField(max_length=100)
    value = models.TextField()
    valuescore = models.FloatField()

    class Meta:
        unique_together = ('company', 'year', 'fieldid')  # Add this constraint
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['fieldname']),
            models.Index(fields=['pillar']),
            models.Index(fields=['valuescore']),
        ]

    def __str__(self):
        return f"{self.company.ticker} | {self.year} | {self.fieldname} = {self.valuescore}"