"""
Tests for the data_loader module
"""
import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dashboard.data_loader import (
    get_projects,
    get_project_list,
    get_kpi_summary,
    get_engagement_trends,
    get_topic_distribution,
    get_sentiment_distribution,
    get_team_capacity,
    get_automation_opportunities,
    get_project_health_distribution
)


class TestDataLoader:
    """Test cases for data_loader functions"""
    
    def test_get_projects_returns_dataframe(self):
        """Test that get_projects returns a DataFrame"""
        df = get_projects()
        assert df is not None
        assert hasattr(df, 'columns')
    
    def test_get_project_list_returns_list(self):
        """Test that get_project_list returns a list of dicts"""
        projects = get_project_list()
        assert isinstance(projects, list)
        if len(projects) > 0:
            assert 'label' in projects[0]
            assert 'value' in projects[0]
    
    def test_get_kpi_summary_returns_dict(self):
        """Test that get_kpi_summary returns expected keys"""
        kpis = get_kpi_summary()
        assert isinstance(kpis, dict)
        expected_keys = [
            'total_engagements', 
            'total_messages', 
            'total_tickets',
            'open_tickets',
            'resolution_rate'
        ]
        for key in expected_keys:
            assert key in kpis, f"Missing key: {key}"
    
    def test_get_kpi_summary_with_project_filter(self):
        """Test that get_kpi_summary works with project filter"""
        kpis = get_kpi_summary(project_id="PROJ-ALPHA")
        assert isinstance(kpis, dict)
        assert kpis['total_engagements'] == 1  # Single project
    
    def test_get_engagement_trends_returns_dataframe(self):
        """Test that get_engagement_trends returns a DataFrame"""
        df = get_engagement_trends(days=30)
        assert df is not None
        assert hasattr(df, 'columns')
        assert 'date' in df.columns or len(df) == 0
    
    def test_get_topic_distribution_returns_dataframe(self):
        """Test that get_topic_distribution returns expected format"""
        df = get_topic_distribution()
        assert df is not None
        assert 'Topic' in df.columns
        assert 'Count' in df.columns
    
    def test_get_sentiment_distribution_returns_dict(self):
        """Test that get_sentiment_distribution returns a dict"""
        dist = get_sentiment_distribution()
        assert isinstance(dist, dict)
        # Should have sentiment categories
        assert len(dist) > 0
    
    def test_get_team_capacity_returns_dataframe(self):
        """Test that get_team_capacity returns expected columns"""
        df = get_team_capacity()
        assert df is not None
        assert 'Person' in df.columns
        assert 'Utilization' in df.columns
    
    def test_get_automation_opportunities_returns_list(self):
        """Test that get_automation_opportunities returns a list"""
        opportunities = get_automation_opportunities()
        assert isinstance(opportunities, list)
        if len(opportunities) > 0:
            opp = opportunities[0]
            assert 'title' in opp
            assert 'description' in opp
            assert 'impact' in opp
            assert 'savings' in opp
    
    def test_get_project_health_distribution_returns_dict(self):
        """Test that get_project_health_distribution returns expected format"""
        dist = get_project_health_distribution()
        assert isinstance(dist, dict)
        # Should have health categories
        assert 'On Track' in dist or len(dist) > 0


class TestDataLoaderEdgeCases:
    """Test edge cases and error handling"""
    
    def test_kpi_summary_with_nonexistent_project(self):
        """Test KPI summary with a project that doesn't exist"""
        kpis = get_kpi_summary(project_id="NONEXISTENT-PROJECT")
        assert isinstance(kpis, dict)
        # Should still return valid structure, just with zero/default values
    
    def test_engagement_trends_with_zero_days(self):
        """Test engagement trends with 0 days"""
        df = get_engagement_trends(days=0)
        assert df is not None
    
    def test_engagement_trends_with_large_days(self):
        """Test engagement trends with large number of days"""
        df = get_engagement_trends(days=365)
        assert df is not None
