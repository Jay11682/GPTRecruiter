from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import re
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate_candidate():
    data = request.json
    job_description = data['job_description']
    resume_text = data['resume_text']

    prompt = f"""You are a recruiter for a staffing company. Your job is to evaluate whether a particular candidate applying for a job is a good fit. You'll find information below about the candidate in the [Candidate Resume] section. You'll find information below about the job in the [Job Description] section. You have three goals: 1. Evaluate the candidate on a scale of 1-10 where 10 is a perfect fit who meets all the requirements and 1 the candidate does not seem like a good fit. Be as nuanced as possible using decimals in your evaluation. Preferred qualifications are a bonus, but required skills are the focus of your score. An 'Ideal' skill is the same as a preferred skill. If a required skill says 'or', then only one of those skills listed is necessary for them to meet that requirement. Take preferred location of candidate, location of the job, and work history into account. They shouldn't have huge gaps between jobs. Remember we are dealing with 100s of resumes a day as a recruiter and your scores should not be too generous; only one can get the placement. Anyone with all the required skills should score above a 7, preferred skills should push this up further. 2. Write a summary of any reasons to not you would hire this person in 12 words or less. 3. Respond to this request based on the [Response Format] section below.\n[Candidate Resume]\n{resume_text}\n[Job Description]\n{job_description}\n\nImportant:\n[Response Format]\nquality_score: #.## \n reject_reason: (Brief reasoning.) for the score given followed by a period. Make sure its in round brackets Be specific. Do not add ANY extra output besides anything outlined in the response format section."""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful recruiting assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    response_text = str(response)
    print(response_text)
    quality_match = re.search(r'quality_score: (\d+\.\d+)', response_text)
    quality_score = float(quality_match.group(1)) if quality_match else 0.0

    reject_match = re.search(r'reject_reason:\s*(.*?)(?=, role)', response_text, re.DOTALL)
    reject_reason = reject_match.group(1).strip().rstrip("'") if reject_match else f"Error getting reject reason."

    return jsonify({'quality_score': quality_score, 'reject_reason': reject_reason})

if __name__ == '__main__':
    app.run(debug=True)