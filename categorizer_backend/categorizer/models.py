from django.db import models as dj_models


class Transaction(dj_models.Model):
    identifier = dj_models.TextField(unique=True)
    amount = dj_models.IntegerField()
    date = dj_models.DateField()
    merchant = dj_models.TextField(null=True, blank=True)
    comments = dj_models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} // {self.amount}/{self.merchant} // {self.comments}"


class Category(dj_models.Model):
    name = dj_models.TextField(unique=True)

    def __str__(self):
        return self.name


class CategoryPattern(dj_models.Model):
    pattern = dj_models.TextField(unique=True)
    category = dj_models.ForeignKey(
        to=Category,
        related_name="category_patterns",
        on_delete=dj_models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.pattern}"


class CategorizedTransaction(dj_models.Model):
    transaction = dj_models.ForeignKey(
        to=Transaction,
        related_name="categorized_transactions",
        on_delete=dj_models.PROTECT,
    )
    category = dj_models.ForeignKey(
        to=Category,
        related_name="categorized_transactions",
        on_delete=dj_models.PROTECT,
        null=True,
        blank=True,
    )
    pattern = dj_models.ForeignKey(
        to=CategoryPattern,
        related_name="categorized_transactions",
        on_delete=dj_models.PROTECT,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.transaction}"
