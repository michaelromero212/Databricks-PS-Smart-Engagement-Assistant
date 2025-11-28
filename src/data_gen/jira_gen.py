import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker()

JIRA_STATUSES = ["Open", "In Progress", "Review", "Done"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
ISSUE_TYPES = ["Bug", "Story", "Task", "Epic"]

def generate_jira_data(project_id, num_tickets=20, start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
        
    tickets = []
    users = [fake.first_name() for _ in range(5)]
    
    for i in range(num_tickets):
        created_at = start_date + timedelta(days=random.randint(0, 20))
        updated_at = created_at + timedelta(days=random.randint(1, 10))
        
        status = random.choice(JIRA_STATUSES)
        # Ensure updated_at is not in future if status is done
        if updated_at > datetime.now():
            updated_at = datetime.now()
            
        ticket = {
            "ticket_id": f"{project_id}-{i+100}",
            "project_id": project_id,
            "summary": fake.sentence(nb_words=6, variable_nb_words=True),
            "description": fake.paragraph(nb_sentences=3),
            "status": status,
            "priority": random.choice(PRIORITIES),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat(),
            "assignee": random.choice(users),
            "story_points": random.choice([1, 2, 3, 5, 8, 13])
        }
        tickets.append(ticket)
        
    return tickets
