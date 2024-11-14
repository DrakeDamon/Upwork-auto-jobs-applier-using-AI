import json
import os
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Constants
API_TOKEN = os.environ.get('APIFY_API_TOKEN')
ACTOR_ID = "username~your-actor-name"  # Replace with your actor's ID
DESIRED_RATE = "15"  # Desired rate in USD per hour

# Job Scraper Prompt Template
SCRAPER_PROMPT_TEMPLATE = """
Extract the following data from this page content:

- **Job Title**
- **Location**
- **Skills Required**: Focus on AI Agent Development, Virtual Assistant Design, NLP, Machine Learning, Chatbot Programming, Conversational AI, Python, JavaScript, TensorFlow, PyTorch, Dialogflow
- **Budget**: Ensure the rate is at least $15 per hour
- **Job Type**: Only consider Contract or Part-Time jobs
- **Client Rating**

<content>
{markdown_content}
</content>

Format the extracted data in a JSON format for easy parsing.
"""

# Job Scoring Prompt Template
SCORE_JOBS_PROMPT_TEMPLATE = """
You are a job matching expert specializing in jobs related to:

1. **Skills**: AI Agent Development, Virtual Assistant Design, NLP, Machine Learning, Chatbot Programming, Conversational AI, Python, JavaScript, TensorFlow, PyTorch, Dialogflow
2. **Experience Level**: Intermediate to Expert in AI and Software Development
3. **Project Type**: AI-driven solutions, chatbot services, virtual assistant projects
4. **Rate**: Ensure the job pays at least $15 per hour, and evaluate it against your desired rate of {desired_rate}.
5. **Job Type**: Only consider Contract or Part-Time jobs
6. **Client History**: Prefer clients with a track record in tech projects, high spending, and longevity on Upwork.

For each job, assign a score from 1 to 10 based on how well it matches these criteria:

Freelancer Profile:
<profile>
{profile}
</profile>

Jobs to evaluate:
{jobs}
"""

# Cover Letter Generation Prompt Template
GENERATE_COVER_LETTER_PROMPT_TEMPLATE = """
# ROLE
You are an Upwork cover letter specialist, focusing on highlighting qualifications like:
- AI Agent Development
- Virtual Assistant Design
- Expertise in NLP and Machine Learning
- Proficiency in Python, JavaScript, TensorFlow, PyTorch

Freelancer Profile:
<profile>
{profile}
</profile>

# SOP
1. Address the job's needs, especially those related to AI development and virtual assistants.
2. Illustrate how your background in AI and related technologies meets these needs.
3. Show enthusiasm for creating innovative AI solutions.
4. Specifically mention your availability for contract or part-time work and your minimum rate of $15 per hour.
5. Keep the letter concise, under 150 words.
6. Integrate job-related keywords naturally.

Job Description:
<job_description>
{job_description}
</job_description>

# **IMPORTANT**
* My name is: {your_name}; include it at the end of the letters.
* Follow the example letter format and structure.
* Do not invent information not present in my profile.
"""

# Call Script Generation Prompt Template
GENERATE_CALL_SCRIPT_PROMPT_TEMPLATE = """
You are a freelance interview preparation coach. Create a call script for discussing these qualifications:

- **Skills**: AI Agent Development, Virtual Assistant Design, NLP, Machine Learning, Chatbot Programming, Python, JavaScript, TensorFlow, PyTorch, Dialogflow
- **Experience**: Projects involving AI conversational agents, virtual assistants, or similar tech solutions
- **Availability**: Emphasize your interest in contract or part-time work
- **Rate**: Mention that you expect a rate of at least $15 per hour

### Job Description:
<job_description>
{job_description}
</job_description>

### Instructions:
1. Introduction highlighting your qualifications in AI and virtual assistant technology, and your flexibility for contract or part-time work.
2. Key points on how your experience matches the job, especially in creating AI solutions.
3. Potential questions about your experience with NLP, machine learning, and development tools.
4. Questions you might ask about the AI project scope, expected outcomes, integration details, and confirmation of the hourly rate.

Return your final output in markdown format.
"""

# Intro Message Generation Prompt Template
GENERATE_INTRO_MESSAGE_PROMPT_TEMPLATE = """
Your role is to craft an introductory message for a freelancer to potential clients on Upwork, focusing on AI agent development and related fields:

**Profile Details:**
<profile>
{profile}
</profile>

**Job Details:**
- Title: {job_title}
- Skills Required: {skills_required}

**Instructions:**
- Introduce yourself professionally, using your name: {your_name}.
- Briefly highlight your expertise in AI agent development, virtual assistants, NLP, Machine Learning, etc.
- Express interest in the job and how your skills align with the job requirements.
- Mention your availability for contract or part-time work.
- State your minimum rate of $15 per hour.
- Keep the message concise, aiming for no more than 100 words.
- End with a call to action, inviting the client to discuss the project further.
- Use a friendly yet professional tone.
"""