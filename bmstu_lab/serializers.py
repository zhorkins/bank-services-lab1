from rest_framework import serializers
from .models import BankService, BankRequest, BankServiceInRequest, User


class BankServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankService
        fields = ['id', 'name', 'balance_account', 'description', 'image', 'video', 'is_deleted', 'price']


class BankServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankService
        fields = ['name', 'balance_account', 'description', 'price']


class BankServiceInRequestSerializer(serializers.ModelSerializer):
    service = BankServiceSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BankServiceInRequest
        fields = ['id', 'request', 'service', 'service_id', 'bank_account']
        read_only_fields = ['id', 'request']


class BankRequestSerializer(serializers.ModelSerializer):
    items = BankServiceInRequestSerializer(source='bankserviceinrequest_set', many=True, read_only=True)
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    moderator_name = serializers.CharField(source='moderator.username', read_only=True)

    class Meta:
        model = BankRequest
        fields = ['id', 'status', 'created_at', 'formed_at', 'completed_at',
                  'client', 'client_name', 'moderator', 'moderator_name', 'total_cost', 'items']
        read_only_fields = ['id', 'status', 'created_at', 'formed_at', 'completed_at',
                            'client', 'moderator', 'client_name', 'moderator_name', 'total_cost']


class BankRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankRequest
        fields = []


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user