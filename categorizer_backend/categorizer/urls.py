from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

import categorizer.views as views


urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:id>/', views.CategoryDetail.as_view()),
    path('transactions/', views.TransactionList.as_view()),
    path('transactions/<str:identifier>/', views.TransactionDetail.as_view()),
    path('transactions_window/', views.TransactionListWindow.as_view()),
    path('categorized_transactions/', views.CategorizedTransactionList.as_view()),
    path('categorized_transactions/<int:id>/', views.CategorizedTransactionDetail.as_view()),
    path('categorized_transactions_window/', views.CategorizedTransactionListWindow.as_view()),
    path('cost_stats/', views.CostStatView.as_view()),
]
