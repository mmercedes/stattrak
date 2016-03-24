from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'sendReport',
                  'first_name', 'last_name', 'bio', 'password',
                  'pic', 'rating', 'is_admin', 'confirm_password')

        read_only_fields = ('created_at', 'rating', 'is_admin')
                  
        def create(self, validated_data):
            return Account.objects.create(**validated_data)
                  
        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.pic = validated_data.get('pic', instance.pic)
            instance.sendReport = validated_data.get('sendReport', instance.sendReport)
            instance.save()
            
            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)
            
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()
                
                update_session_auth_hash(self.context.get('request'), instance)
                
                return instance
