import categorizer.models as models


def find_category_pattern(transaction: models.Transaction) -> models.CategoryPattern | None:                                              
    for pattern in models.CategoryPattern.objects.all().iterator():                                         
        if (
            pattern.pattern.lower() in transaction.merchant.lower() or
            pattern.pattern.lower() in transaction.comments.lower()
            ):
            return pattern