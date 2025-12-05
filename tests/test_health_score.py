"""
Tests for the health_score module
"""
import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.health_score import (
    calculate_health_score,
    get_health_scores_by_project,
    get_health_breakdown,
    HealthScore,
    WEIGHTS
)


class TestHealthScore:
    """Test cases for health score calculation"""
    
    def test_calculate_health_score_returns_health_score_object(self):
        """Test that calculate_health_score returns a HealthScore object"""
        result = calculate_health_score()
        assert isinstance(result, HealthScore)
        assert hasattr(result, 'score')
        assert hasattr(result, 'trend')
        assert hasattr(result, 'breakdown')
        assert hasattr(result, 'status')
    
    def test_health_score_range(self):
        """Test that health score is between 0 and 100"""
        result = calculate_health_score()
        assert 0 <= result.score <= 100
    
    def test_health_score_trend_values(self):
        """Test that trend is one of the expected values"""
        result = calculate_health_score()
        assert result.trend in ['↑', '↓', '→']
    
    def test_health_score_status_values(self):
        """Test that status is one of the expected values"""
        result = calculate_health_score()
        expected_statuses = ['Excellent', 'Good', 'At Risk', 'Critical']
        assert result.status in expected_statuses
    
    def test_health_score_breakdown_has_all_components(self):
        """Test that breakdown contains all weighted components"""
        result = calculate_health_score()
        for component in WEIGHTS.keys():
            assert component in result.breakdown, f"Missing component: {component}"
    
    def test_weights_sum_to_one(self):
        """Test that weights sum to 1.0"""
        total_weight = sum(WEIGHTS.values())
        assert abs(total_weight - 1.0) < 0.001, f"Weights sum to {total_weight}, expected 1.0"
    
    def test_calculate_health_score_with_project_filter(self):
        """Test health score calculation for a specific project"""
        result = calculate_health_score(project_id="PROJ-ALPHA")
        assert isinstance(result, HealthScore)
        assert 0 <= result.score <= 100


class TestHealthScoresAggregate:
    """Test cases for aggregate health score functions"""
    
    def test_get_health_scores_by_project_returns_list(self):
        """Test that get_health_scores_by_project returns a list"""
        result = get_health_scores_by_project()
        assert isinstance(result, list)
    
    def test_health_scores_by_project_structure(self):
        """Test structure of health scores by project"""
        result = get_health_scores_by_project()
        if len(result) > 0:
            item = result[0]
            assert 'project_id' in item
            assert 'score' in item
            assert 'trend' in item
            assert 'status' in item
    
    def test_health_scores_sorted_by_score(self):
        """Test that results are sorted by score descending"""
        result = get_health_scores_by_project()
        if len(result) > 1:
            scores = [item['score'] for item in result]
            assert scores == sorted(scores, reverse=True)


class TestHealthBreakdown:
    """Test cases for health breakdown function"""
    
    def test_get_health_breakdown_returns_dict(self):
        """Test that get_health_breakdown returns a dict"""
        result = get_health_breakdown("PROJ-ALPHA")
        assert isinstance(result, dict)
    
    def test_health_breakdown_has_components(self):
        """Test that breakdown has components list"""
        result = get_health_breakdown("PROJ-ALPHA")
        assert 'components' in result
        assert isinstance(result['components'], list)
    
    def test_health_breakdown_components_have_required_fields(self):
        """Test that each component has required fields"""
        result = get_health_breakdown("PROJ-ALPHA")
        for component in result['components']:
            assert 'name' in component
            assert 'score' in component
            assert 'weight' in component


class TestStatusLabels:
    """Test status label assignment logic"""
    
    def test_excellent_status_threshold(self):
        """Test that scores >= 85 get 'Excellent' status"""
        # This tests the internal logic - we can't directly test private functions
        # but we can verify the overall behavior
        result = calculate_health_score()
        if result.score >= 85:
            assert result.status == 'Excellent'
        elif result.score >= 70:
            assert result.status == 'Good'
        elif result.score >= 50:
            assert result.status == 'At Risk'
        else:
            assert result.status == 'Critical'
