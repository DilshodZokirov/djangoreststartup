from rest_framework.serializers import ModelSerializer

from apps.users.models import Company


# name = models.CharField(max_length=200)
#     description = models.CharField(max_length=400, null=True, blank=True)
#     company_background = models.FileField(upload_to="company", null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_at", null=True, blank=True)
class GetCompanyModelSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
            "description",
            "company_background",
            "created_by"
        ]
