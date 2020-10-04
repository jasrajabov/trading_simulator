from rest_framework import serializers
from w_app.models import TradeData


class TradeDataSerializer(serializers.ModelSerializer):
    """serializer for Trade data"""

    class Meta:
        model = TradeData
        fields = ['id', 'fix', 'symbol', 'quantity', 'order_type', 'direction',
            'exec_date']
