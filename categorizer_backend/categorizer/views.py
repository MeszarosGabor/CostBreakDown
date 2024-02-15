import collections
import datetime

from django.shortcuts import render
from rest_framework import generics, viewsets, response, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action

import categorizer.models as models
import categorizer.serializers as serializers


class CategoryList(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
    def get_object(self, queryset=None):
        return models.Category.objects.filter(name=self.kwargs.get("name")).first()


class TransactionList(generics.ListCreateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    
    def get_object(self, queryset=None):
        return models.Transaction.objects.filter(identifier=self.kwargs.get("identifier")).first()


class TransactionListWindow(generics.ListCreateAPIView):
    serializer_class = serializers.TransactionSerializer

    def list(self, request, *args, **kwargs):
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")

        if not start_date or not end_date:
            return response.Response({"data":[]})
        start_date = [int(x) for x in start_date.split("-")]
        end_date = [int(x) for x in end_date.split("-")]

        objects = models.Transaction.objects.filter(
            date__gte=datetime.date(*start_date), 
            date__lte=datetime.date(*end_date),
            ).all()
        serialized = self.get_serializer(objects, many=True)
        return response.Response({"data":serialized.data})


class CategorizedTransactionList(generics.ListCreateAPIView):
    queryset = models.CategorizedTransaction.objects.all()
    serializer_class = serializers.CategorizedTransactionSerializer


class CategorizedTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.CategorizedTransaction.objects.prefetch_related("category").prefetch_related("transaction").all()
    serializer_class = serializers.CategorizedTransactionSerializer
    
    def get_object(self, queryset=None):
        return models.CategorizedTransaction.objects.prefetch_related("category").prefetch_related("transaction").filter(transaction__identifier=self.kwargs.get("identifier")).first()


class CategorizedTransactionListWindow(generics.ListCreateAPIView):
    serializer_class = serializers.CategorizedTransactionSerializer

    def list(self, request, *args, **kwargs):
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")
        category = request.GET.get("category", "")

        if not start_date or not end_date:
            return response.Response({"data":[]})
        start_date = [int(x) for x in start_date.split("-")]
        end_date = [int(x) for x in end_date.split("-")]

        queryset = models.CategorizedTransaction.objects.prefetch_related("category").prefetch_related("transaction").filter(
            transaction__date__gte=datetime.date(*start_date), 
            transaction__date__lte=datetime.date(*end_date),
            )
        if category:
            queryset = queryset.filter(category__name=category)
        objects = queryset.all()

        serialized = self.get_serializer(objects, many=True)
        return response.Response({"data":serialized.data})
    

# TODO: this should be done via modelViewSet
class CostStatView(APIView):
    def get(self, request):
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")
        if not start_date or not end_date:
            return response.Response({"error": "missing start or end date"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = [int(x) for x in start_date.split("-")]
       

        end_date = [int(x) for x in end_date.split("-")]

        targets = models.CategorizedTransaction.objects.select_related("transaction").select_related("category").filter(
            transaction__date__gte=datetime.date(*start_date),
            transaction__date__lte=datetime.date(*end_date))

        collector = collections.defaultdict(int)
        for target in targets:
            category = target.category.name if target.category else "misc"
            collector[category] += target.transaction.amount

        return response.Response(collector)
