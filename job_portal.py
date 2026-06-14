from dataclasses import dataclass
from typing import List


@dataclass
class JobOpening:
    """Represents a job opening on the portal."""
    job_id: str
    title: str
    company: str
    location: str
    offered_ctc_min: float  # in lakhs
    offered_ctc_max: float
    required_years: int
    required_skills: List[str]
    description: str
    job_url: str
    posted_date: str

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "offered_ctc_min": self.offered_ctc_min,
            "offered_ctc_max": self.offered_ctc_max,
            "required_years": self.required_years,
            "required_skills": self.required_skills,
            "description": self.description,
            "job_url": self.job_url,
            "posted_date": self.posted_date,
        }


class JobPortal:
    """Simulates a job portal with available job listings."""

    def __init__(self):
        self.jobs: List[JobOpening] = self._create_sample_jobs()

    def _create_sample_jobs(self) -> List[JobOpening]:
        """Create sample Data Engineer jobs in Bangalore."""
        return [
            JobOpening(
                job_id="JOB001",
                title="Data Engineer - II",
                company="TechBridge Analytics",
                location="Bangalore",
                offered_ctc_min=18.0,
                offered_ctc_max=24.0,
                required_years=3,
                required_skills=["Python", "SQL", "ETL", "Spark"],
                description="We are looking for a Data Engineer with 3+ years of experience in building ETL pipelines.",
                job_url="https://jobs.techbridge.com/de-ii",
                posted_date="2026-06-10",
            ),
            JobOpening(
                job_id="JOB002",
                title="Senior Data Engineer",
                company="CloudData Labs",
                location="Bangalore",
                offered_ctc_min=28.0,
                offered_ctc_max=35.0,
                required_years=5,
                required_skills=["Python", "AWS", "Kafka", "Spark"],
                description="Senior Data Engineer to lead data infrastructure initiatives.",
                job_url="https://jobs.clouddata.com/senior-de",
                posted_date="2026-06-12",
            ),
            JobOpening(
                job_id="JOB003",
                title="Data Engineer",
                company="InsightWorks",
                location="Bangalore",
                offered_ctc_min=15.0,
                offered_ctc_max=20.0,
                required_years=2,
                required_skills=["Python", "SQL", "ETL"],
                description="Data Engineer for data warehousing and ETL processes.",
                job_url="https://jobs.insightworks.com/de",
                posted_date="2026-06-08",
            ),
            JobOpening(
                job_id="JOB004",
                title="Data Engineer (Remote)",
                company="GlobalTech Solutions",
                location="Remote",
                offered_ctc_min=20.0,
                offered_ctc_max=28.0,
                required_years=3,
                required_skills=["Python", "GCP", "BigQuery", "SQL"],
                description="Data Engineer - fully remote role.",
                job_url="https://jobs.globaltech.com/de-remote",
                posted_date="2026-06-11",
            ),
            JobOpening(
                job_id="JOB005",
                title="Data Engineer",
                company="DataCorp India",
                location="Bangalore",
                offered_ctc_min=22.0,
                offered_ctc_max=30.0,
                required_years=4,
                required_skills=["Python", "SQL", "Spark", "AWS", "Kafka"],
                description="Data Engineer for real-time data processing pipelines.",
                job_url="https://jobs.datacorp.com/de",
                posted_date="2026-06-13",
            ),
        ]

    def search_by_location(self, location: str) -> List[JobOpening]:
        """Search jobs by location."""
        return [job for job in self.jobs if job.location.lower() == location.lower()]

    def search_all(self) -> List[JobOpening]:
        """Get all available jobs."""
        return self.jobs
