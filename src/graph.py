import pandas as pd
from typing import List, Dict, Any
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from colorama import Fore, Style
from .utils import (
    run_apify_actor,  # Assuming this function was added to utils based on prompts.py
    process_jobs,
    generate_document  # This function will be used for cover letter and intro message generation
)

COVER_LETTERS_FILE = "./files/cover_letter.txt"

class GraphState(TypedDict):
    job_title: str
    scraped_jobs: List[Dict[str, Any]]
    matches: List[Dict[str, Any]]
    job_description: str
    cover_letter: str
    intro_message: str
    num_matches: int

class UpworkAutomation:
    def __init__(self, profile, num_jobs=20):
        self.profile = profile
        self.number_of_jobs = num_jobs
        self.graph = self.build_graph()

    async def scrape_upwork_jobs(self, state: GraphState) -> GraphState:
        """
        Scrape jobs from Upwork based on job title provided.

        @param state: The current state of the application.
        @return: Updated state with scraped jobs.
        """
        print(Fore.YELLOW + f"----- Scraping Upwork jobs for: {state['job_title']} -----\n" + Style.RESET_ALL)
        job_title = state['job_title']
        scraped_jobs = await run_apify_actor(job_title)
        print(Fore.GREEN + f"----- Scraped {len(scraped_jobs)} jobs -----\n" + Style.RESET_ALL)
        return {**state, "scraped_jobs": scraped_jobs}

    def score_scraped_jobs(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "----- Scoring scraped jobs -----\n" + Style.RESET_ALL)
        processed_jobs = process_jobs(state['scraped_jobs'])
        matches =[job for job in processed_jobs if job.get('score', 0) >= 7]
        return {**state, "matches": matches, "num_matches": len(matches)}

    def check_for_job_matches(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "----- Checking for remaining job matches -----\n" + Style.RESET_ALL)
        return state

    def need_to_process_matches(self, state: GraphState) -> str:
        """
        Check if there are any job matches.

        @param state: The current state of the application.
        @return: "empty" if no job matches, otherwise "process".
        """
        if len(state["matches"]) == 0:
            print(Fore.RED + "No job matches remaining\n" + Style.RESET_ALL)
            return "No matches"
        else:
            print(Fore.GREEN + f"There are {len(state['matches'])} Job matches remaining to process\n" + Style.RESET_ALL)
            return "Process jobs"

    def generate_job_application_content(self, state: GraphState) -> GraphState:
        return state

    async def generate_cover_letter(self, state: GraphState) -> GraphState:
        """
        Generate cover letter based on the job description and the profile.

        @param state: The current state of the application.
        @return: Updated state with generated cover letter.
        """
        print(Fore.YELLOW + "----- Generating cover letter -----\n" + Style.RESET_ALL)
        job = state['matches'][-1]
        cover_letter = await generate_document("cover_letter", job['title'], job['description'], job['skills_required'], self.profile)
        return {**state, "job_description": job['description'], "cover_letter": cover_letter}

    async def generate_intro_message(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "----- Generating intro message -----\n" + Style.RESET_ALL)
        job = state['matches'][-1]
        intro_message = await generate_document("intro_message", job['title'], job['description'], job['skills_required'], self.profile)
        return {**state, "intro_message": intro_message}

    def save_job_application_content(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "----- Saving cover letter & script -----\n" + Style.RESET_ALL)
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(COVER_LETTERS_FILE, "a") as file:
            file.write("\n" + "=" * 80 + "\n")
            file.write(f"DATE: {timestamp}\n")
            file.write("=" * 80 + "\n\n")

            file.write("### Job Description ###\n")
            file.write(state["job_description"] + "\n\n")

            file.write("### Cover Letter ###\n")
            file.write(state["cover_letter"] + "\n\n")

            file.write("### Intro Message ###\n")
            file.write(state["intro_message"] + "\n")

            file.write("\n" + "/" * 100 + "\n")

        # Remove already processed job
        state["matches"].pop()
        return {"matches": state["matches"]}

    def build_graph(self) -> StateGraph:
        graph = StateGraph(GraphState)

        # create all required nodes
        graph.add_node("scrape_upwork_jobs", self.scrape_upwork_jobs)
        graph.add_node("score_scraped_jobs", self.score_scraped_jobs)
        graph.add_node("check_for_job_matches", self.check_for_job_matches)
        graph.add_node("generate_job_application_content", self.generate_job_application_content)
        graph.add_node("generate_cover_letter", self.generate_cover_letter)
        graph.add_node("generate_intro_message", self.generate_intro_message)
        graph.add_node("save_job_application_content", self.save_job_application_content)

        # Link nodes to complete workflow
        graph.set_entry_point("scrape_upwork_jobs")
        graph.add_edge("scrape_upwork_jobs", "score_scraped_jobs")
        graph.add_edge("score_scraped_jobs", "check_for_job_matches")
        graph.add_conditional_edges(
            "check_for_job_matches",
            self.need_to_process_matches,
            {"Process jobs": "generate_job_application_content", "No matches": END},
        )
        graph.add_edge("generate_job_application_content", "generate_cover_letter")
        graph.add_edge("generate_job_application_content", "generate_intro_message")
        graph.add_edge("generate_cover_letter", "save_job_application_content")
        graph.add_edge("generate_intro_message", "save_job_application_content")
        graph.add_edge("save_job_application_content", "check_for_job_matches")

        return graph.compile()

    async def run(self, job_title: str) -> GraphState:
        print(Fore.BLUE + "----- Running Upwork Jobs Automation -----\n" + Style.RESET_ALL)
        config = {"recursion_limit": 1000}
        state = await self.graph.invoke({"job_title": job_title}, config)
        return state