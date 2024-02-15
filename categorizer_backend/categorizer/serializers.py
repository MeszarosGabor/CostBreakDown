from rest_framework import serializers

import categorizer.models as models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name',]


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
        fields = ['transaction', 'category', 'pattern']

    
    transaction = TransactionSerializer()
    category = CategorySerializer()
    pattern = CategoryPatternSerializer()
