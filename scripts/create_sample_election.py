import os
import sys
from datetime import datetime, timedelta

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app import create_app, db
from app.models.ballot import Ballot
from app.models.candidate import Candidate

def create_sample_election():
    """Create a sample election with multiple positions and candidates"""
    app = create_app()
    
    with app.app_context():
        # Check if sample election already exists
        existing_ballot = Ballot.query.filter_by(title="Sample University Elections 2025").first()
        if existing_ballot:
            print("Sample election already exists!")
            return
        
        # Create the ballot (main election)
        now = datetime.utcnow()
        end_date = now + timedelta(days=7)  # Election runs for 7 days
        
        sample_election = Ballot(
            title="Sample University Elections 2025",
            description="This is a sample election for the University Student Council with multiple positions.",
            start_date=now,
            end_date=end_date,
            is_active=True,
            ballot_type="university",
            requires_verification=True,
            verification_method="id"
        )
        
        # Generate verification key
        sample_election.verification_key = sample_election.generate_verification_hash()
        
        db.session.add(sample_election)
        db.session.flush()  # Flush to get the ID without committing
        
        # Create positions and candidates
        positions = {
            "President": ["John Smith", "Maria Rodriguez", "Ahmed Hassan"],
            "Vice President": ["Michael Johnson", "Sarah Lee", "Robert Chen"],
            "Secretary": ["Emily Davis", "Daniel Brown", "Jessica Wilson"],
            "Treasurer": ["David Miller", "Grace Taylor", "Samuel Jackson"],
            "Events Coordinator": ["Olivia Moore", "William Clark", "Sophia Martinez"]
        }
        
        # Add all candidates for each position
        for position, candidates in positions.items():
            for candidate_name in candidates:
                candidate = Candidate(
                    name=candidate_name,
                    position=position,
                    manifesto=f"Manifesto for {candidate_name} running for {position}. This is a sample manifesto text that outlines the candidate's platform and goals for the position.",
                    photo_url="",  # No photo for sample data
                    ballot_id=sample_election.id
                )
                db.session.add(candidate)
        
        # Commit all changes
        db.session.commit()
        print(f"Sample election '{sample_election.title}' created successfully with {len(positions)} positions and {sum(len(c) for c in positions.values())} candidates.")
        print(f"Election is active until: {end_date}")
        print("\nTo view this election:")
        print("1. Register an account or log in")
        print("2. Navigate to 'Current Elections'")
        print("3. Select the sample election to see positions and candidates")

if __name__ == "__main__":
    create_sample_election()
