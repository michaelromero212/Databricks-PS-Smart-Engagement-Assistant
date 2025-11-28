import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker()

SLACK_TEMPLATES = [
    "Hey @{user}, can you check the pipeline for {project}?",
    "I'm seeing an error in the bronze layer ingestion: {error}",
    "Great news! The UAT sign-off is complete.",
    "Does anyone have the latest architecture diagram for {client}?",
    "Meeting in 5 mins: {link}",
    "Deployment failed in staging. Logs attached.",
    "Can we reschedule the daily standup?",
    "Kudos to @{user} for fixing that critical bug!",
    "Is there documentation on how to use the new feature?",
    "Client is asking for an update on the migration status."
]

TECHNICAL_ERRORS = [
    "AnalysisException: Table not found",
    "OutOfMemoryError: Java heap space",
    "Timeout waiting for connection",
    "Invalid access token",
    "Schema mismatch in column 'customer_id'"
]

def generate_slack_data(project_id, num_messages=50, start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    
    messages = []
    users = [fake.first_name() for _ in range(5)]
    
    current_time = start_date
    
    for _ in range(num_messages):
        # Advance time randomly
        current_time += timedelta(minutes=random.randint(1, 120))
        
        # 20% chance of starting a new thread, 80% chance of reply if thread exists
        is_thread_reply = random.random() < 0.4 and len(messages) > 0
        
        if is_thread_reply:
            parent = random.choice(messages)
            thread_id = parent['thread_id'] if parent['thread_id'] else parent['message_id']
            # If parent didn't have a thread_id, it started a thread.
            # But wait, if parent['thread_id'] is None, it's a top level message.
            # If we reply to it, we use its message_id as thread_id.
            if not parent['thread_id']:
                 thread_id = parent['message_id']
        else:
            thread_id = None
            
        user = random.choice(users)
        template = random.choice(SLACK_TEMPLATES)
        content = template.format(
            user=random.choice(users),
            project=project_id,
            error=random.choice(TECHNICAL_ERRORS),
            client=fake.company(),
            link=fake.url()
        )
        
        # Add some emojis - REMOVED per user request
        # if random.random() < 0.3:
        #     content += " " + random.choice(["🚀", "✅", "🔥", "👀", "👍"])

        msg = {
            "message_id": str(uuid.uuid4()),
            "project_id": project_id,
            "user_id": user,
            "timestamp": current_time.isoformat(),
            "content": content,
            "thread_id": thread_id,
            "channel_name": "general",
            "is_bot": False
        }
        messages.append(msg)
        
    return messages
