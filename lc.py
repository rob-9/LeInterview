##REDUNDANT (BACKUP)


import google.generativeai as genai
GEMINI_API_KEY = "AIzaSyBE-bdUQUfKW4L9UKualT10yzxk2AGeFes"





genai.configure(api_key= GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")



def get_response_from_gemini(problem_name):
    try:
        response = model.generate_content(f"very beriefly disply the problem {problem_name}from leetcode and one sample output")
        return response.text
    except Exception as e:
        print("Unable to get content")

