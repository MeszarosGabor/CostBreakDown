from django.contrib import admin, messages

import categorizer.models as models
import categorizer.utils as utils

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    ordering = ("-date", "amount")
    list_display = (
        "date",
        "amount",
        "merchant",
        "comments",
    )
    search_fields = ("merchant", "comments")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
      "name",
    )
    search_fields = ("name",)


@admin.register(models.CategoryPattern)
class CategoryPatternAdmin(admin.ModelAdmin):
    ordering = ("category", "pattern")
    list_display = (
      "pattern",
      "category",
    )
    search_fields = ("pattern", "category__name")
    list_select_related = ("category",)
    autocomplete_fields = ("category",)


@admin.register(models.CategorizedTransaction)
class CategorizedTransactionAdmin(admin.ModelAdmin):
    ordering = ("category", "transaction")
    list_display = (
      "category",
      "transaction",
    )
    search_fields = ("category__name","transaction__merchant")
    list_select_related = ("category",)
    autocomplete_fields = ("category",)

    actions = (
        "recalculate_categories",
    )


    @admin.action(description="Recalculate Categories")
    def recalculate_categories(self, request, queryset):
        for categorized_transaction in queryset:
            try:
              error_msg = None
              pattern = utils.find_category_pattern(categorized_transaction.transaction)
              new_category = pattern.category if pattern else None
              _, created = models.CategorizedTransaction.objects.update_or_create(
                  transaction=categorized_transaction.transaction,
                  defaults={
                      "category":new_category,
                  }
              )
            except Exception as exc:
                error_msg = str(exc)

            self.message_user(
                request,
                error_msg or f"Successfully recalculated Category, new category is {new_category}",
                messages.ERROR if error_msg else messages.SUCCESS
            )
  