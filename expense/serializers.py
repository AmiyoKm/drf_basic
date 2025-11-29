from rest_framework import serializers

from expense.models import Transactions


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
        read_only_fields = ["user_id"]
