from rest_framework import serializers

import categorizer.models as models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["id", "name"]
        extra_kwargs = {
            'name': {'validators': []},  # Disable the unique validator for the update case
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ['identifier', 'amount', 'date', 'merchant', 'comments']


class CategoryPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryPattern
        fields = ["pattern", "category"]

    pattern = serializers.CharField()
    category = CategorySerializer()


class CategorizedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategorizedTransaction
        fields = ['id', 'transaction', 'category', 'category_id', 'pattern']

    
    transaction = TransactionSerializer()
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        source="category",
        write_only=True,
    )
    pattern = CategoryPatternSerializer()
