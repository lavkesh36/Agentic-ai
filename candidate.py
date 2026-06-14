from dataclasses import dataclass
from typing import List


@dataclass
class CandidateProfile:
    """Represents a candidate's resume data."""
    name: str
    email: str
    phone: str
    current_ctc: float  # in lakhs
    expected_ctc_min: float
    expected_ctc_max: float
    years_of_experience: int
    current_role: str
    current_company: str
    skills: List[str]
    preferred_locations: List[str]
    education: str

    def matches_recruiter_requirements(self, required_years: int, required_skills: List[str]) -> bool:
        """Check if candidate meets recruiter's minimum requirements."""
        if self.years_of_experience < required_years:
            return False
        for skill in required_skills:
            if skill.lower() not in [s.lower() for s in self.skills]:
                return False
        return True

    def matches_job_offer(self, offered_ctc_min: float, offered_ctc_max: float, job_location: str) -> bool:
        """Check if job matches candidate's expectations."""
        if job_location not in self.preferred_locations:
            return False
        if offered_ctc_max < self.expected_ctc_min:
            return False
        if offered_ctc_min > self.expected_ctc_max:
            return False
        return True

    def skill_match_score(self, required_skills: List[str]) -> int:
        """Score how many required skills the candidate has (0-100)."""
        if not required_skills:
            return 100
        matched = sum(1 for skill in required_skills if skill.lower() in [s.lower() for s in self.skills])
        return int((matched / len(required_skills)) * 100)

    def ctc_fit_score(self, offered_ctc_min: float, offered_ctc_max: float) -> int:
        """Score how well the CTC aligns (0-100)."""
        # Best fit when offered CTC is in candidate's expected range
        if self.expected_ctc_min <= offered_ctc_max and offered_ctc_min <= self.expected_ctc_max:
            overlap_min = max(self.expected_ctc_min, offered_ctc_min)
            overlap_max = min(self.expected_ctc_max, offered_ctc_max)
            overlap = overlap_max - overlap_min
            expected_range = self.expected_ctc_max - self.expected_ctc_min
            return int((overlap / expected_range) * 100) if expected_range > 0 else 100
        return 0
