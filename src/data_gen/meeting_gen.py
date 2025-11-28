import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker()

MEETING_TYPES = ["Daily Standup", "Weekly Sync", "Sprint Planning", "Retrospective", "Client Update"]

def generate_meeting_data(project_id, num_meetings=5, start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
        
    meetings = []
    
    for _ in range(num_meetings):
        meeting_date = start_date + timedelta(days=random.randint(0, 30))
        
        meeting_id = str(uuid.uuid4())
        meeting = {
            "meeting_id": meeting_id,
            "project_id": project_id,
            "date": meeting_date.isoformat(),
            "title": f"{random.choice(MEETING_TYPES)} - {project_id}",
            "attendees": ", ".join([fake.first_name() for _ in range(4)]),
            "agenda": "- Review progress\n- Discuss blockers\n- Plan next steps",
            "notes": fake.paragraph(nb_sentences=5)
        }
        meetings.append(meeting)
        
    return meetings

def generate_action_items(source_id, source_type="meeting"):
    items = []
    num_items = random.randint(0, 3)
    
    for _ in range(num_items):
        item = {
            "item_id": str(uuid.uuid4()),
            "source_id": source_id,
            "source_type": source_type,
            "description": fake.sentence(nb_words=5),
            "owner": fake.first_name(),
            "due_date": (datetime.now() + timedelta(days=random.randint(1, 14))).isoformat(),
            "status": random.choice(["Open", "In Progress", "Done"])
        }
        items.append(item)
        
    return items
