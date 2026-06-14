from agent import Agent
from candidate import CandidateProfile


def main() -> None:
    # Create a sample candidate profile (simulating resume parsing)
    candidate = CandidateProfile(
        name="Rajesh Kumar",
        email="rajesh.kumar@email.com",
        phone="+91-9876543210",
        current_ctc=18.0,  # in lakhs
        expected_ctc_min=22.0,
        expected_ctc_max=30.0,
        years_of_experience=4,
        current_role="Data Engineer",
        current_company="TechCorp",
        skills=["Python", "SQL", "Spark", "ETL", "AWS", "Kafka"],
        preferred_locations=["Bangalore", "Remote"],
        education="B.Tech in Computer Science",
    )

    # Create agent with candidate profile
    agent = Agent("JobSearchBot", candidate=candidate)
    agent.set_goal("Apply for Data Engineer roles in Bangalore")

    initial_state = {
        "status": "idle",
    }

    final_state = agent.run(initial_state, max_steps=15)

    print("=" * 80)
    print("AGENT JOB APPLICATION REPORT")
    print("=" * 80)
    
    print("\nCandidate Profile:")
    print(f"  Name: {candidate.name}")
    print(f"  Current: {candidate.current_role} at {candidate.current_company}")
    print(f"  Experience: {candidate.years_of_experience} years")
    print(f"  Current CTC: {candidate.current_ctc} L")
    print(f"  Expected CTC: {candidate.expected_ctc_min}-{candidate.expected_ctc_max} L")
    print(f"  Skills: {', '.join(candidate.skills)}")
    print(f"  Preferred Locations: {', '.join(candidate.preferred_locations)}")

    print("\nTask Execution:")
    for task in agent.tasks:
        print(f"  - {task['name']}: {task['status']}")

    print("\nMatching Results:")
    matched = final_state.get("matched_jobs", [])
    print(f"  Total jobs in portal: {len(final_state.get('all_jobs', []))}")
    print(f"  Matched jobs: {len(matched)}")

    if matched:
        print(f"\n  Top 3 Best Matches:")
        for i, match in enumerate(final_state.get("top_matches", []), 1):
            job = match["job"]
            print(f"    {i}. {job.title} at {job.company}")
            print(f"       Location: {job.location} | CTC: {job.offered_ctc_min}-{job.offered_ctc_max} L")
            print(f"       Match Score: {match['overall_score']:.1f}% (Skills: {match['skill_score']:.0f}%, CTC: {match['ctc_score']:.0f}%)")

    print("\nDrafted Applications:")
    for i, app in enumerate(final_state.get("applications", []), 1):
        print(f"  {i}. {app['title']} at {app['company']} ({app['offered_ctc']} L)")
        print(f"     Match Score: {app['match_score']}")
        print(f"     Link: {app['job_url']}")

    print("\n" + "=" * 80)
    print("END OF REPORT")
    print("=" * 80)


if __name__ == "__main__":
    main()
