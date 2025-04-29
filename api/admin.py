from django.contrib import admin
from .models import CandidateProfile, CandidateEvaluation

# Register your models here
admin.site.register(CandidateProfile)
admin.site.register(CandidateEvaluation)
