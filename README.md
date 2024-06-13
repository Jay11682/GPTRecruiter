# GPT Recruiter

## What is GPT Recruiter
GPT Recruiter is a prescreening tool to assist recruiters or those looking to improve their resume. A score from 1-10 is given based on how good of a fit a resume is for a given job description. This score is supported with a short excerpt from ChatGPT explaining the reasoning for the score received.

## Getting Started
Clone the repo and create a file in the main folder called ".env" which contains your API key in this format: <br/>
OPENAI_API_KEY=sk-... your OpenAI API Key

To run, simply type "python3 app.py" and navigate to http://127.0.0.1:5000

**If you are having trouble running, you may need to install the following dependencies using pip**

* pip install flask-cors 
* pip install python-dotenv
* pip install flask openai

![Image of the tool](images/image.png)
