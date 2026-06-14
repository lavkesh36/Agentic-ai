from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from candidate import CandidateProfile
from job_portal import JobOpening, JobPortal


@dataclass
class Action:
    name: str
    description: str
    tool: Optional[str] = None
    payload: Optional[str] = None


@dataclass
class Tool:
    name: str
    description: str
    function: Callable[[str, Dict[str, Any], Dict[str, Any]], str]

    def execute(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        return self.function(task, state, context)


class Agent:
    """A job-application agent with candidate profile and two-way preference matching."""

    def __init__(self, name: str, candidate: Optional[CandidateProfile] = None):
        self.name = name
        self.goal = ""
        self.candidate = candidate
        self.target_role = "Data Engineer"
        self.location = "Bangalore"
        self.tasks: List[Dict[str, str]] = []
        self.memory: List[str] = []
        self.history: List[str] = []
        self.tools = self._build_tools()
        self.job_portal = JobPortal()

    def _build_tools(self) -> Dict[str, Tool]:
        return {
            "load_profile": Tool(
                "load_profile",
                "Load and validate candidate profile from resume.",
                self._load_profile,
            ),
            "job_search": Tool(
                "job_search",
                "Search for open roles matching candidate location preference.",
                self._job_search,
            ),
            "match": Tool(
                "match",
                "Two-way matching: filter by recruiter requirements and candidate expectations.",
                self._match_roles,
            ),
            "draft_application": Tool(
                "draft_application",
                "Draft tailored application for matched roles.",
                self._draft_application,
            ),
            "review": Tool(
                "review",
                "Review results and summarize next actions.",
                self._review,
            ),
        }

    def set_goal(self, goal: str) -> None:
        self.goal = goal.strip()
        self._parse_goal()
        self.memory.append(f"Goal set: {self.goal}")
        self.history.append(f"Agent received goal: {self.goal}")
        self.decompose_goal()

    def _parse_goal(self) -> None:
        lower = self.goal.lower()
        if "data engineer" in lower:
            self.target_role = "Data Engineer"
        if "bangalore" in lower or "bengaluru" in lower:
            self.location = "Bangalore"
        elif "remote" in lower:
            self.location = "Remote"

    def decompose_goal(self) -> None:
        if not self.goal:
            self.tasks = []
            return

        self.tasks = [
            {"name": "Load candidate profile", "status": "pending"},
            {"name": "Search for open roles", "status": "pending"},
            {"name": "Match roles with preferences", "status": "pending"},
            {"name": "Draft applications", "status": "pending"},
            {"name": "Review and summarize", "status": "pending"},
        ]

        self.memory.append(f"Decomposed goal into {len(self.tasks)} job application tasks.")
        self.history.append(f"Task list: {[task['name'] for task in self.tasks]}")

    def perceive(self, state: Dict[str, Any], task: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        observation = {
            "status": state.get("status", "unknown"),
            "task": task["name"] if task else "none",
            "candidate_loaded": self.candidate is not None,
            "target_role": self.target_role,
            "location": self.location,
        }
        self.memory.append(f"Perceived: {observation}")
        return observation

    def plan_task(self, task: Dict[str, str], observation: Dict[str, Any]) -> List[Action]:
        if task["status"] == "done":
            return []

        self.memory.append(f"Planning task: '{task['name']}'.")
        lower_name = task["name"].lower()

        if "load" in lower_name or "profile" in lower_name:
            return [
                Action("Load Profile", "Parse and validate candidate resume data.", tool="load_profile", payload="resume"),
            ]

        if "search" in lower_name:
            return [
                Action("Search Jobs", "Query job portal for open roles.", tool="job_search", payload=self.location),
            ]

        if "match" in lower_name:
            return [
                Action("Match", "Filter by recruiter and candidate preferences.", tool="match", payload="preferences"),
            ]

        if "draft" in lower_name:
            return [
                Action("Draft Applications", "Create tailored application materials.", tool="draft_application", payload="drafts"),
            ]

        if "review" in lower_name or "summarize" in lower_name:
            return [
                Action("Review", "Summarize results and next steps.", tool="review", payload="summary"),
            ]

        return []

    def act(self, action: Action, state: Dict[str, Any]) -> Dict[str, Any]:
        if action.tool and action.tool in self.tools:
            tool = self.tools[action.tool]
            outcome = tool.execute(action.payload or action.name, state, state)
        else:
            outcome = f"Performed '{action.name}'."

        state["status"] = f"{action.name} completed"
        state["last_action"] = action.name

        self.history.append(outcome)
        self.memory.append(outcome)
        return state

    def _load_profile(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        if not self.candidate:
            return "No candidate profile provided. Using default profile for demo."
        state["candidate"] = self.candidate
        state["current_exp"] = self.candidate.years_of_experience
        state["current_ctc"] = self.candidate.current_ctc
        return f"Loaded candidate profile: {self.candidate.name} ({self.candidate.current_role} at {self.candidate.current_company}) with {self.candidate.years_of_experience} years of experience."

    def _job_search(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        jobs = self.job_portal.search_all()
        state["all_jobs"] = jobs
        return f"Found {len(jobs)} job openings for {self.target_role} across all locations."

    def _match_roles(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        if not self.candidate:
            return "Cannot match without candidate profile."

        all_jobs = state.get("all_jobs", [])
        matched_jobs = []

        for job in all_jobs:
            # Recruiter filter: candidate must meet requirements
            if not self.candidate.matches_recruiter_requirements(job.required_years, job.required_skills):
                continue

            # Candidate filter: job must match expectations
            if not self.candidate.matches_job_offer(job.offered_ctc_min, job.offered_ctc_max, job.location):
                continue

            # Score the match
            skill_score = self.candidate.skill_match_score(job.required_skills)
            ctc_score = self.candidate.ctc_fit_score(job.offered_ctc_min, job.offered_ctc_max)
            exp_score = min(100, (self.candidate.years_of_experience / job.required_years) * 100)
            overall_score = (skill_score + ctc_score + exp_score) / 3

            matched_jobs.append({
                "job": job,
                "overall_score": overall_score,
                "skill_score": skill_score,
                "ctc_score": ctc_score,
            })

        # Sort by overall score
        matched_jobs.sort(key=lambda x: x["overall_score"], reverse=True)
        state["matched_jobs"] = matched_jobs
        state["top_matches"] = matched_jobs[:3]

        return f"Matched {len(matched_jobs)} jobs after filtering by recruiter requirements and candidate preferences. Top 3 selected for applications."

    def _draft_application(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        if not self.candidate:
            return "Cannot draft applications without candidate profile."

        top_matches = state.get("top_matches", [])
        applications = []

        for match in top_matches:
            job = match["job"]
            skills_match = ", ".join(job.required_skills)
            application = {
                "job_id": job.job_id,
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "offered_ctc": f"{job.offered_ctc_min}-{job.offered_ctc_max} L",
                "match_score": f"{match['overall_score']:.1f}%",
                "resume_summary": f"{self.candidate.name} - {self.candidate.current_role} with {self.candidate.years_of_experience} years of experience specializing in {', '.join(self.candidate.skills[:3])}.",
                "cover_letter_intro": f"I am interested in the {job.title} position at {job.company}. With my background in {skills_match}, I am well-positioned to contribute to your team.",
                "job_url": job.job_url,
            }
            applications.append(application)

        state["applications"] = applications
        return f"Drafted {len(applications)} tailored applications for top-matched roles."

    def _review(self, task: str, state: Dict[str, Any], context: Dict[str, Any]) -> str:
        if not self.candidate:
            return "No candidate profile to review."

        summary = [
            f"Candidate: {self.candidate.name}",
            f"Current Role: {self.candidate.current_role} ({self.candidate.years_of_experience} yrs exp)",
            f"Current CTC: {self.candidate.current_ctc} L | Expected: {self.candidate.expected_ctc_min}-{self.candidate.expected_ctc_max} L",
            f"Skills: {', '.join(self.candidate.skills)}",
            f"Preferred Locations: {', '.join(self.candidate.preferred_locations)}",
            f"",
            f"Job Search Results:",
            f"- Total jobs found: {len(state.get('all_jobs', []))}",
            f"- Matched jobs: {len(state.get('matched_jobs', []))}",
            f"- Applications drafted: {len(state.get('applications', []))}",
        ]

        if state.get("applications"):
            summary.append("\nTop Matches:")
            for i, app in enumerate(state.get("applications", []), 1):
                summary.append(f"  {i}. {app['title']} at {app['company']} ({app['offered_ctc']} L) - Score: {app['match_score']}")

        return "\n".join(summary)

    def evaluate_task(self, state: Dict[str, Any], task: Dict[str, str]) -> bool:
        if "review" in task["name"].lower() or state.get("last_action") == "Review":
            task["status"] = "done"
            return True
        return False

    def reflect(self) -> None:
        observation = f"Completed agent run with {len(self.tasks)} tasks and {len(self.memory)} memory entries."
        self.memory.append(observation)
        self.history.append(observation)

    def run(self, state: Dict[str, Any], max_steps: int = 15) -> Dict[str, Any]:
        step_count = 0

        for task in self.tasks:
            if step_count >= max_steps:
                self.history.append("Max steps reached.")
                break

            observation = self.perceive(state, task)
            actions = self.plan_task(task, observation)

            for action in actions:
                if step_count >= max_steps:
                    break
                state = self.act(action, state)
                step_count += 1

            self.evaluate_task(state, task)

        self.reflect()
        return state
