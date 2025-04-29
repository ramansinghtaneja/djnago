from django.db import models

class CandidateProfile(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    education_details = models.TextField(help_text="Degrees, Institutions, Years, and CGPA")
    location = models.CharField(max_length=255, blank=True, null=True)
    employment_details = models.TextField(help_text="Year of Experience and Work Done")
    total_years_of_experience = models.CharField(max_length=50, help_text="Total Experience (Range)")
    technical_skills = models.TextField(help_text="List of Technical Skills")
    soft_skills = models.TextField(help_text="List of Soft Skills")
    certifications = models.TextField(help_text="List of Certifications, Licenses, Credentials", blank=True, null=True)
    profile_links = models.TextField(help_text="Links of Profiles like LinkedIn, GitHub, etc.", blank=True, null=True)
    projects = models.TextField(help_text="Details of Projects or Notable Work", blank=True, null=True)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)

    def __str__(self):
        return self.full_name
    
class CandidateEvaluation(models.Model):
    candidate = models.OneToOneField(CandidateProfile, on_delete=models.CASCADE, related_name='evaluation')
    score = models.IntegerField(help_text="Score given during evaluation", blank=True, null=True)
    remarks = models.TextField(help_text="Remarks on the candidate", blank=True, null=True)

    def __str__(self):
        return f"Evaluation for {self.candidate.full_name}"