# from django.db import models
#
# from apps.users.models import User
# from distributive.models import BaseModel
#
#
# class Company(BaseModel):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=400, null=True, blank=True)
#     company_background = models.FileField(upload_to="company", null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_at", null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.name} - {self.description}"
