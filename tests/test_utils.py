"""
Unit tests for utility functions in mixbpm.py
"""
import pytest
import sys
import os

# Add parent directory to path to import mixbpm
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mixbpm import calculer_pret_interet_fixe


class TestCalculerPretInteretFixe:
    """Tests for calculer_pret_interet_fixe function"""
    
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_basic(self):
        """Test basic loan calculation with standard parameters"""
        result = calculer_pret_interet_fixe(10000, 5.0, 12)
        
        assert "mensualite" in result
        assert "total_a_rembourser" in result
        assert "principal_mensuel" in result
        assert "interet_mensuel" in result
        assert "interets_totaux" in result
        
        # Check that calculated values are positive
        assert result["mensualite"] > 0
        assert result["total_a_rembourser"] > 0
        assert result["principal_mensuel"] > 0
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_zero_duration(self):
        """Test loan calculation with zero duration"""
        result = calculer_pret_interet_fixe(10000, 5.0, 0)
        
        assert result["mensualite"] == 0.0
        assert result["total_a_rembourser"] == 0.0
        assert result["principal_mensuel"] == 0.0
        assert result["interet_mensuel"] == 0.0
        assert result["interets_totaux"] == 0.0
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_negative_duration(self):
        """Test loan calculation with negative duration"""
        result = calculer_pret_interet_fixe(10000, 5.0, -12)
        
        assert result["mensualite"] == 0.0
        assert result["total_a_rembourser"] == 0.0
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_zero_rate(self):
        """Test loan calculation with zero interest rate"""
        result = calculer_pret_interet_fixe(10000, 0.0, 12)
        
        # With zero interest, monthly payment should equal principal/duration
        expected_mensualite = 10000 / 12
        assert abs(result["mensualite"] - expected_mensualite) < 0.01
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_interest_years(self):
        """Test that interest is correctly distributed across years"""
        # 36 month loan
        result = calculer_pret_interet_fixe(10000, 5.0, 36)
        
        # All three years should have interest
        assert result["interets_annee1"] > 0
        assert result["interets_annee2"] > 0
        assert result["interets_annee3"] > 0
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_short_loan(self):
        """Test loan calculation for duration less than 12 months"""
        result = calculer_pret_interet_fixe(10000, 5.0, 6)
        
        # Only first year should have interest
        assert result["interets_annee1"] > 0
        assert result["interets_annee2"] == 0.0
        assert result["interets_annee3"] == 0.0
        
    @pytest.mark.unit
    def test_calculer_pret_interet_fixe_return_types(self):
        """Test that all returned values are properly rounded"""
        result = calculer_pret_interet_fixe(10000, 5.5, 24)
        
        # All values should be floats rounded to 2 decimal places
        for key, value in result.items():
            assert isinstance(value, float)
            # Check that there are at most 2 decimal places
            assert value == round(value, 2)
