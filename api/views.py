from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.http import JsonResponse
from .get_similarity import query_vector_db , display_candidates , filter_candidates , filter_candidates_ , get_report , clean_response_data , get_hm_questions
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CandidateProfile , CandidateEvaluation
from django.conf import settings

from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal, InvalidOperation
from .emailer import sendemail
import pandas as pd



def home(request):
    return render(request, 'api/base.html')

def testt(request):
    return render(request, 'api/index.html')


def assessment_details(request):
    # Fetch all assessments
    assessments = CandidateEvaluation.objects.all()
    
    # Prepare context to pass to the template
    context = {
        'assessments': assessments
    }
    
    return render(request, 'api/assessment_details.html', context)


@csrf_exempt
def get_summery(request):
    if request.method == "POST":

         
    
        try:
            data = json.loads(request.body)

            job_description = data.get('job_description', '')
            candidate_data  = data.get('candidate_data', {})
            if job_description and candidate_data:
                candidate_data_experience = candidate_data.get('experience', '')
                candidate_data_skills = candidate_data.get('technical_skills', '')
                candidate_data_exp = ' '
                result_data = get_report(job_description , candidate_data_experience, candidate_data_skills, candidate_data_exp)
                final_result_data = clean_response_data(result_data)
                
                return JsonResponse({"result": final_result_data})

            else:
                return JsonResponse({"error": "No data provided"}, status=400)

           

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def profile_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            job_description = data.get('job_description', '')

            if job_description:
                resume_id = query_vector_db(job_description)

                candidates = display_candidates(resume_id)

                

                

                if len(candidates) > 0:
                    
                    result_data = []
                    for candidate in candidates:
                        candidate_data = {
                            'full_name': candidate.full_name,
                            'email': candidate.email,
                            'location': candidate.location,
                            'technical_skills': candidate.technical_skills,
                            'experience': candidate.total_years_of_experience
                        }
                        result_data.append(candidate_data)
                    
            
            
                return JsonResponse({"result": result_data})

            else:
                return JsonResponse({"error": "No data provided"}, status=400)

            return JsonResponse({"result": job_description})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def profile_list_filter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            job_description = data.get('job_description', '')
            filter_data = data.get('filter_data', {})

            if filter_data:

                resume_id = query_vector_db(job_description)

                # candidates = filter_candidates(resume_id, filter_data)

                candidates = filter_candidates_(resume_id, filter_data)

                result_data = "fail"

                if len(candidates) > 0:
                    result_data = "sucess"

                    result_data = []
                    for candidate in candidates:
                        candidate_data = {
                            'full_name': candidate.full_name,
                            'email': candidate.email,
                            'location': candidate.location,
                            'technical_skills': candidate.technical_skills,
                            'experience': candidate.total_years_of_experience
                        }
                        result_data.append(candidate_data)
                    
                    
                return JsonResponse({"result": result_data})

            else:
                return JsonResponse({"error": "No data provided"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    


def preprocessing(request):

    file_name="candidates (31).xlsx"
    file_path="C:\\Users\\singhram\\Downloads\\"+file_name
    df=pd.read_excel(file_path)
    df= df[:1]
    df["interview_link"] = '<a href="' + df["interview_link"] + '">' + df["interview_link"] + "</a>"
    df.rename(columns={'full_name': 'Name','email':'Email','phone_number':'Phone Number','interview_status':'Interview Status',\
                    'interview_date':'Interview Date', 'interview_time':'Interview Time','interview_link':'Interview Link'}, inplace=True)
    dfc=df.style.set_table_styles([
    {'selector': 'th, td',
    'props': [('border', '0.5px solid black')]},
    {'selector' : '',
    'props' : [('border', '0.5px solid black')]},
    {'selector' : 'tr',
    'props' : [('border', '0.5px solid black')]}
    ])
    styled_dfc = dfc.hide(axis="index")
    mail_content="""
    <html>
    <head></head>
    <body>
    Dear Candidate, <br>
    Congratulation! Your interview has been scheduled with Zinnia. Please refer to the following details. <br><br>
    {0}<br><br>
    Regards,<br>
    HR Zinnia
    </body>
    </html>
    """.format(styled_dfc.to_html())
    return mail_content





@csrf_exempt
def profile_shortlist(request):
    if request.method == "POST":
        try:
            # mail_content= preprocessing()
            # res= sendemail(mail_content,settings.SUBJECT, None ,settings.RECEIVERS,ATTACHMENTS=[])
            # print(res)
            # # Load the incoming JSON data from the request
            data = json.loads(request.body)
    
            candidates_data = data.get('candidates', [])

            # # If no candidates are provided, return an error
            if not candidates_data:
                return JsonResponse({"error": "No candidates selected."}, status=400)
            
            # # return JsonResponse({"error": f" {len(candidates_data)}"}, status=200)

            candidate_top = candidates_data[0]
            email = candidate_top.get('email', '')
            password=""
            if (email == 'k.khare@outlook.com' or email== 'abdulateek36@gmail.com' or  email=='viveksaha.arjun@gmail.com'):
                password="7VX7ra9Q"
            if (email == 'shreehari3@yahoo.com' or email=='suhanisjain23@gmail.com' or email=='kanika.bansal.met20@itbhu.ac.in' \
                or email=='arya.vivek@gmail.com' or email=='it.amitagarwal@gmail.com' or email=='aayushsinghla@gmail.com'):
                password="1234"

            name = candidate_top.get('name', None) 
            remarks = candidate_top.get('remarks', '')
            phoneNumber = candidate_top.get('phoneNumber','')
            interviewStatus = candidate_top.get('interviewStatus','')
            interviewDate = candidate_top.get('interviewDate','')
            interviewTime= candidate_top.get('interviewTime','')
            
            candidate_data = {
                "full_name": [name],  
                "email": [email],
                "phone_number": [phoneNumber],
                "interview_status": [interviewStatus],
                "interview_date": [interviewDate],
                "interview_time": [interviewTime],
                "interview_link": ["http://ai-resume-zinnia.vercel.app"],
                "password": password
            }

            df = pd.DataFrame(candidate_data)

            if 'interview_link' in df.columns:
                df["interview_link"] = '<a href="' + df["interview_link"] + '">' + df["interview_link"] + "</a>"

            
            df.rename(columns={
                'full_name': 'Name',
                'email': 'Email',
                'phone_number': 'Phone Number',
                'interview_status': 'Interview Status',
                'interview_date': 'Interview Date',
                'interview_time': 'Interview Time',
                'interview_link': 'Interview Link',
                "password": "password"
            }, inplace=True)
            

            dfc=df.style.set_table_styles([
            {'selector': 'th, td',
            'props': [('border', '0.5px solid black')]},
            {'selector' : '', 
            'props' : [('border', '0.5px solid black')]},
            {'selector' : 'tr', 
            'props' : [('border', '0.5px solid black')]}
            ])
            styled_dfc = dfc.hide(axis="index")

            mail_content="""
            <html>
            <head></head>
            <body>
            Dear Candidate, <br>
            Congratulation! Your interview has been scheduled with Zinnia. Please refer to the following details . <br><br>
            {0}<br><br>
            Regards,<br>
            HR Zinnia
            </body>
            </html>
            """.format(styled_dfc.to_html())
            SUBJECT= "Interview Scheduled with Zinnia"
            RECEIVERS=['abhay.prajapati@zinnia.com','anant.vijay@zinnia.com','ramanjot.singh@zinnia.com']

            if len(df)>0:
                 print('email sending process begins')
                 res=sendemail(mail_content, SUBJECT, df, RECEIVERS)
                 print(res)
                 print('email sending process ends')

            if(len(data)):
                return JsonResponse({"message": "Data processed successfully"}, status=200)

        except Exception as e:
            # In case of an error, return the error message
            return JsonResponse({"error": str(e)}, status=400)
    
    # If the request method is not POST, return an error
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
                




# def assessment_details(request):
   
#     assessments = CandidateEvaluation.objects.all()
    
    
#     context = {
#         'assessments': assessments
#     }
    
#     return render(request, 'storepdf/assessment_details.html', context)


@csrf_exempt
def get_candidate_questions(request):
    if request.method == "POST":
        try:
           
            data = json.loads(request.body)

            # Validate required fields
            job_description = data.get('job_description', '').strip()
            skills = data.get('skills', '').strip()
            employment_details = data.get('employment_details', '').strip()
            experience = data.get('experience', '').strip()

            if not job_description or not skills or not employment_details or not experience:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Call function to generate hiring manager questions
            result_data = get_hm_questions(job_description, experience, skills, employment_details)

            # Return generated questions or report
            return JsonResponse({'questions': result_data}, status=200)

        except json.JSONDecodeError:
            # Handle case where JSON data is malformed
            
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            # General error handling
            
            return JsonResponse({'error': 'Internal server error'}, status=500)



