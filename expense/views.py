from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from expense.models import Transactions
from expense.serializers import TransactionsSerializer


class TransactionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("REQUEST USER", request.user)
        queryset = Transactions.objects.filter(user_id=request.user)
        serializer = TransactionsSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(
                {"message": "Transaction created successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=400)


class TransactionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Transactions.objects.get(id=pk, user_id=user)
        except Transactions.DoesNotExist:
            return None

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"message": "Transaction not found"}, status=404)
        serializer = TransactionsSerializer(transaction)
        return Response({"data": serializer.data})

    def patch(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"message": "Transaction not found"}, status=404)
        serializer = TransactionsSerializer(
            transaction, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Transaction updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"message": "Transaction not found"}, status=404)
        transaction.delete()
        return Response({"message": "Transaction deleted successfully"})

    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response({"message": "Transaction not found"}, status=404)
        serializer = TransactionsSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Transaction updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=400)

