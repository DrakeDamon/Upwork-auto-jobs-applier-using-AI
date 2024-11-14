from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class JobType(str, Enum):
    FIXED = "Fixed"
    HOURLY = "Hourly"

class JobInformation(BaseModel):
    title: str = Field(description="The title of the job")
    description: str = Field(description="The full description of the job")
    job_type: JobType = Field(description="The type of the job (Fixed or Hourly)")
    experience_level: str = Field(description="The experience level of the job")
    duration: Optional[str] = Field(description="The estimated duration of the job")
    budget: Optional[str] = Field(
        description="""
        The payment rate for the job. Can be in several formats:
        - Hourly rate range: '$15.00-$25.00' or '$15-$25'
        - Fixed rate: '$500' or '$1,000'
        - Budget range: '$500-$1,000'
        All values should include the '$' symbol.
        """
    )
    client_rating: Optional[float] = Field(description="The client's rating")
    skills_required: List[str] = Field(description="List of skills required for the job")
    job_url: str = Field(description="The URL link to the job on Upwork")

class JobScore(BaseModel):
    job_id: str = Field(description="The id of the job, ideally the job_url")
    score: int = Field(description="The score of the job")

class JobScores(BaseModel):
    matches: List[JobScore] = Field(description="The list of job scores")

class CoverLetter(BaseModel):
    letter: str = Field(description="The generated cover letter")

class CallScript(BaseModel):
    script: str = Field(description="The generated call script or intro message")

class GraphState(BaseModel):
    job_title: str = Field(description="The title of the job being searched")
    scraped_jobs: List[Dict[str, Any]] = Field(description="List of scraped jobs in dictionary format")
    matches: List[JobInformation] = Field(description="List of jobs that match the criteria after scoring")
    job_description: str = Field(description="Description of the current job being processed")
    cover_letter: str = Field(description="Generated cover letter for the current job")
    intro_message: str = Field(description="Generated intro message for the current job")
    num_matches: int = Field(description="Number of job matches found")