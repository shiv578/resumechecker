
# # genai.configure(api_key="AIzaSyCCimEeNl8dN8-lHdLg7FmPKKnnGyw9JuM")
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyCCimEeNl8dN8-lHdLg7FmPKKnnGyw9JuM")


# def generate_resume(jd_text, resume_text):

#     model = genai.GenerativeModel("gemini-1.5-flash")

#     prompt = f"""
# You are an expert resume writer.

# Analyze the job description and resume.

# Improve the resume:
# - Add missing skills
# - Improve projects
# - Make ATS optimized

# Return ONLY the final resume.

# JOB DESCRIPTION:
# {jd_text}

# RESUME:
# {resume_text}
# """

#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"