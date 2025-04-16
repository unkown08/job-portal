import re 
from rest_framework import serializers

def password_validation(value: str):
    if len(value) < 5:
            raise serializers.ValidationError(
                "Password must be at least 5 characters long" 
            )
    if not re.search(r'[^a-zA-Z0-9]', value):
        raise serializers.ValidationError(
            "Password must have at least one special character" 
        )
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError(
            "Password must have at least one upper case character"
        )
    if not re.search(r'[0-9]', value):
        raise serializers.ValidationError(
            "Password must have at least one number character"
        )