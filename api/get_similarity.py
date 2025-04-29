import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from .models import CandidateProfile
from groq import Groq
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Q
import json
import re

import environ


env = environ.Env()


environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

DB_FAISS_PATH = "api/vectordb/db_faiss"


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)


def query_vector_db(job_description):
   
    job_description = str(job_description)

    
    
    search_results = db.similarity_search(job_description, k=10) 
    
    
    resume_ids = [doc.metadata['resume_id'] for doc in search_results]  
    
    
    return resume_ids





def display_candidates(resume_ids):
    # Ensure that resume_ids is not empty
    if not resume_ids:
        return CandidateProfile.objects.none()

    # Create a Case-When expression to maintain the order of resume_ids
    order_case = Case(
        *[When(id=resume_id, then=Value(index)) for index, resume_id in enumerate(resume_ids)],
        default=Value(len(resume_ids)),  # Ensure all other IDs come after the listed ones
        output_field=IntegerField()
    )

    # Filter CandidateProfile based on resume_ids and order them according to the Case-When expression
    candidates = CandidateProfile.objects.filter(id__in=resume_ids).order_by(order_case)

    return candidates




def filter_candidates(resume_ids, filter_criteria):
    
    candidates = display_candidates(resume_ids)
    candidates_initial = candidates
    
    if filter_criteria.get('skills'):
        
        skills_list = [skill.strip() for skill in filter_criteria['skills'].split(',')]
        
        
        skill_filter = Q()
        for skill in skills_list:
            skill_filter |= Q(technical_skills__icontains=skill)
        
        candidates = candidates.filter(skill_filter)
    
   
    if filter_criteria.get('location'):
        candidates = candidates.filter(location__icontains=filter_criteria['location'])
    
    if filter_criteria.get('experience'):
        candidates = candidates.filter(total_years_of_experience__icontains=filter_criteria['experience'])

    if filter_criteria.get('soft_skills'):
        candidates = candidates.filter(soft_skills__icontains=filter_criteria['soft_skills'])

    if filter_criteria.get('gender'):
        candidates = candidates.filter(gender__icontains=filter_criteria['gender'])

    if filter_criteria.get('employment_details'):
        candidates = candidates.filter(employment_details__icontains=filter_criteria['employment_details'])    

    if filter_criteria.get('education_details'):
        candidates = candidates.filter(education_details__icontains=filter_criteria['education_details'])

    return candidates






def filter_candidates_(resume_ids, filter_criteria):
    # Get initial candidates based on the provided resume_ids
    candidates = display_candidates(resume_ids)
    
    # Store the initial order of candidates
    candidates_initial = list(candidates)  # Convert to list to maintain the order
    
    # Create a map of resume_id to its original position for sorting later
    resume_id_to_position = {candidate.id: idx for idx, candidate in enumerate(candidates_initial)}

    # Apply filters
    if filter_criteria.get('skills'):
        skills_list = [skill.strip() for skill in filter_criteria['skills'].split(',')]
        skill_filter = Q()
        for skill in skills_list:
            skill_filter |= Q(technical_skills__icontains=skill)
        candidates = candidates.filter(skill_filter)

    if filter_criteria.get('location'):
        candidates = candidates.filter(location__icontains=filter_criteria['location'])

    # Handle experience filter
    if filter_criteria.get('experience'):
        experience_input = filter_criteria['experience']
        
        try:
            # If it's a single number, convert it to a range of n-1 to n+1
            if '-' not in experience_input:
                experience_input = int(experience_input)
                lower_limit = experience_input - 1
                upper_limit = experience_input + 1
            else:
                # If range is provided like '3-5', split and convert
                experience_range = experience_input.split('-')
                lower_limit = int(experience_range[0])
                upper_limit = int(experience_range[1])

            filtered_candidates = []
            for candidate in candidates:
                # Candidate experience is stored as "x-y"
                if candidate.total_years_of_experience:
                    experience = candidate.total_years_of_experience.split('-')
                    
                    if len(experience) == 2:
                        candidate_lower_limit = int(experience[0])
                        candidate_upper_limit = int(experience[1])

                        # Check if the candidate's experience range overlaps with the filter criteria range
                        if candidate_upper_limit >= lower_limit and candidate_lower_limit <= upper_limit:
                            filtered_candidates.append(candidate)

            candidates = filtered_candidates

        except ValueError:
            # Handle case if the experience data is incorrectly formatted
            print("Invalid experience range format")
            return []

    if filter_criteria.get('soft_skills'):
        candidates = candidates.filter(soft_skills__icontains=filter_criteria['soft_skills'])

    if filter_criteria.get('gender'):
        candidates = candidates.filter(gender__icontains=filter_criteria['gender'])

    if filter_criteria.get('employment_details'):
        candidates = candidates.filter(employment_details__icontains=filter_criteria['employment_details'])

    if filter_criteria.get('education_details'):
        candidates = candidates.filter(education_details__icontains=filter_criteria['education_details'])
    
    # Now sort the candidates based on their original position in candidates_initial
    sorted_candidates = sorted(candidates, key=lambda x: resume_id_to_position.get(x.id, float('inf')))
    
    return sorted_candidates



client = Groq(api_key=SECRET_KEY)

def extract_report_sections(report_text):
    # Define the regex patterns to extract the three sections
    sections = {
        "positive_points": "",
        "lacking_points": "",
        "overall_suitability": ""
    }

    # Regex patterns to capture the content after each section header
    patterns = {
        "positive_points": r"Positive Points:\s*(.*?)(?=\nLacking Points:|\nOverall Suitability:|\Z)",
        "lacking_points": r"Lacking Points:\s*(.*?)(?=\nOverall Suitability:|\Z)",
        "overall_suitability": r"Overall Suitability:\s*(.*?)(?=\n|\Z)"
    }

    # Loop through the patterns and extract the sections
    for section, pattern in patterns.items():
        match = re.search(pattern, report_text, re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()

    return sections
def get_report(job_description, candidate_data_experience, candidate_data_skills, candidate_data_ex):
    # Step 1: Format the input to send to the model
    messages = [
        {
            "role": "system",
            "content": "You are an AI bot designed to act as a professional resume parser. "
                       "Compare the provided job description with the candidate's experience and skills "
                       "and generate a detailed report, structured in the following way:"
                       "1. Positive Points (strengths based on the job description)."
                       "2. Lacking Points (areas where the candidate's profile does not meet the job requirements)."
                       "Provide the data  with the fields Positive Points: , Lacking Points:  in a concise and readable format."
        },
        {
            "role": "user",
            "content": f"Job Description: {job_description}\n"
                       f"Candidate Experience (Details): {candidate_data_ex}\n"
                       f"Candidate Skills: {candidate_data_skills}\n"
                       f"Candidate Experience (Years): {candidate_data_experience} years\n"
        }
    ]

    # Step 2: Call the chat completion model
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",  # Use the appropriate model for text analysis
        stream=False,
    )

    # Step 3: Extract the response from the model
    report_text = chat_completion.choices[0].message.content

    
    structured_report = extract_report_sections(report_text)

    return structured_report

    


def clean_response_data(data):
    # Remove unnecessary stars and excessive formatting from the data
    cleaned_data = {
        "positive_points": clean_text(data.get("positive_points", "")),
        "lacking_points": clean_text(data.get("lacking_points", "")),
        
    }
    return cleaned_data

def clean_text(text):
    # Clean the text by removing unwanted symbols (like '**')
    # and extra white spaces or line breaks.
    text = text.replace('**', '').strip()
    text = ' '.join(text.split())  # Remove excessive white spaces and new lines
    return text

def get_hm_questions(job_description, candidate_data_experience, candidate_data_skills, candidate_data_ex):
    # Step 1: Format the input to send to the model
    messages = [
        {
            "role": "system",
            "content": "You are an AI bot designed to assist hiring managers by generating interview questions based on the provided job description and the candidate's profile. "
                       "Your task is to analyze the job description, the candidate's experience, and skills, and generate relevant interview questions to help evaluate the candidate for the role. "
                       "These questions should assess the candidate's strengths and weaknesses in relation to the job requirements. "
                       "Make sure the questions are diverse, covering technical, behavioral, lacking points in candidates compared to job description and situational aspects of the candidate's skills and experience."
                       "Dont add any extra text just ask questions nothing else in reposnse and add question number with each question."
        },
        {
            "role": "user",
            "content": f"Job Description: {job_description}\n"
                       f"Candidate Experience (Details): {candidate_data_ex}\n"
                       f"Candidate Skills: {candidate_data_skills}\n"
                       f"Candidate Experience (Years): {candidate_data_experience} years\n"
        }
    ]

    # Step 2: Call the chat completion model
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",  # Use the appropriate model for text analysis
        stream=False,
    )

    # Step 3: Extract the response from the model
    report_text = chat_completion.choices[0].message.content

    
    # structured_report = extract_report_sections(report_text)

    return report_text

    