from rest_framework import serializers

from postings.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer): # forms.ModelForm
    url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'url',
            'id',
            'user',
            'name',
            'address',
            'city',
            'contact',
        ]
        read_only_fields = ['id', 'user']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = UserProfile.objects.filter(name__iexact=value) # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username has already been used")
        return value