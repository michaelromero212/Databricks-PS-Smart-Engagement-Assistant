"""
Tests for mock data generators
"""
import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_gen.slack_gen import generate_slack_data
from src.data_gen.jira_gen import generate_jira_data
from src.data_gen.meeting_gen import generate_meeting_data, generate_action_items


class TestSlackGenerator:
    """Test cases for Slack message generator"""
    
    def test_generate_slack_data_returns_list(self):
        """Test that generate_slack_data returns a list"""
        result = generate_slack_data("PROJ-TEST", num_messages=10)
        assert isinstance(result, list)
        assert len(result) == 10
    
    def test_slack_message_structure(self):
        """Test that generated messages have required fields"""
        result = generate_slack_data("PROJ-TEST", num_messages=1)
        assert len(result) == 1
        msg = result[0]
        
        required_fields = ['message_id', 'project_id', 'user_id', 'timestamp', 'content']
        for field in required_fields:
            assert field in msg, f"Missing field: {field}"
    
    def test_slack_data_project_id_matches(self):
        """Test that project_id in messages matches input"""
        project_id = "PROJ-CUSTOM"
        result = generate_slack_data(project_id, num_messages=5)
        for msg in result:
            assert msg['project_id'] == project_id
    
    def test_slack_data_unique_message_ids(self):
        """Test that message IDs are unique"""
        result = generate_slack_data("PROJ-TEST", num_messages=50)
        message_ids = [msg['message_id'] for msg in result]
        assert len(message_ids) == len(set(message_ids))


class TestJiraGenerator:
    """Test cases for Jira ticket generator"""
    
    def test_generate_jira_data_returns_list(self):
        """Test that generate_jira_data returns a list"""
        result = generate_jira_data("PROJ-TEST", num_tickets=10)
        assert isinstance(result, list)
        assert len(result) == 10
    
    def test_jira_ticket_structure(self):
        """Test that generated tickets have required fields"""
        result = generate_jira_data("PROJ-TEST", num_tickets=1)
        ticket = result[0]
        
        required_fields = ['ticket_id', 'project_id', 'summary', 'status', 'priority']
        for field in required_fields:
            assert field in ticket, f"Missing field: {field}"
    
    def test_jira_ticket_status_valid(self):
        """Test that ticket status is a valid value"""
        result = generate_jira_data("PROJ-TEST", num_tickets=20)
        valid_statuses = ['Open', 'In Progress', 'Done', 'Blocked', 'Review']
        for ticket in result:
            assert ticket['status'] in valid_statuses, f"Invalid status: {ticket['status']}"
    
    def test_jira_ticket_priority_valid(self):
        """Test that ticket priority is a valid value"""
        result = generate_jira_data("PROJ-TEST", num_tickets=20)
        valid_priorities = ['Critical', 'High', 'Medium', 'Low']
        for ticket in result:
            assert ticket['priority'] in valid_priorities, f"Invalid priority: {ticket['priority']}"


class TestMeetingGenerator:
    """Test cases for meeting generator"""
    
    def test_generate_meeting_data_returns_list(self):
        """Test that generate_meeting_data returns a list"""
        result = generate_meeting_data("PROJ-TEST", num_meetings=5)
        assert isinstance(result, list)
        assert len(result) == 5
    
    def test_meeting_structure(self):
        """Test that generated meetings have required fields"""
        result = generate_meeting_data("PROJ-TEST", num_meetings=1)
        meeting = result[0]
        
        required_fields = ['meeting_id', 'project_id', 'date', 'title']
        for field in required_fields:
            assert field in meeting, f"Missing field: {field}"
    
    def test_generate_action_items_returns_list(self):
        """Test that generate_action_items returns a list"""
        result = generate_action_items("MEET-001", "meeting")
        assert isinstance(result, list)
    
    def test_action_item_structure(self):
        """Test that action items have required fields"""
        result = generate_action_items("MEET-001", "meeting")
        if len(result) > 0:
            item = result[0]
            required_fields = ['item_id', 'source_id', 'source_type', 'description']
            for field in required_fields:
                assert field in item, f"Missing field: {field}"


class TestDataGeneratorConsistency:
    """Test consistency across generators"""
    
    def test_generators_produce_consistent_output(self):
        """Test that generators produce consistent output format"""
        slack = generate_slack_data("PROJ-TEST", num_messages=1)
        jira = generate_jira_data("PROJ-TEST", num_tickets=1)
        meetings = generate_meeting_data("PROJ-TEST", num_meetings=1)
        
        # All should be lists
        assert isinstance(slack, list)
        assert isinstance(jira, list)
        assert isinstance(meetings, list)
        
        # All should have project_id
        assert slack[0]['project_id'] == "PROJ-TEST"
        assert jira[0]['project_id'] == "PROJ-TEST"
        assert meetings[0]['project_id'] == "PROJ-TEST"
