from rest_framework import serializers
from w_app.models import TradeData
from . import fix_messages, fix_mapping
import ipdb
import datetime
from django.utils import timezone


class TradeDataSerializer(serializers.ModelSerializer):
    """serializer for Trade data"""

    class Meta:
        model = TradeData
        fields = ['id', 'fix', 'symbol', 'price',
         'quantity', 'order_type', 'direction',
            'exec_date']

    def to_internal_value(self, validated_data):
        fix_message = fix_messages.createNewOrderSinge(
                validated_data['symbol'],
                validated_data['direction'],
                validated_data['order_type'],
                validated_data['quantity'])
        message = {'fix': fix_message.__str__(), 'exec_date': datetime.datetime.now(tz=timezone.utc)}
        validated_data.update(message)
        # ipdb.set_trace()
        return validated_data
