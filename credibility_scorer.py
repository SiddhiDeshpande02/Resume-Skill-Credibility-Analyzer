"""
Skill credibility scoring engine
"""
from config import SCORE_THRESHOLDS


class CredibilityScorer:
    def __init__(self):
        """Initialize credibility scorer"""
        self.thresholds = SCORE_THRESHOLDS
    
    def calculate_skill_score(self, skill_data, evidence_data):
        """
        Calculate credibility score for a skill
        
        Args:
            skill_data: dict with 'skill', 'claim_level'
            evidence_data: dict with 'overall_strength', 'total_score', 'details'
        
        Returns:
            dict with credibility score and explanation
        """
        skill = skill_data['skill']
        claim_level = skill_data['claim_level']
        evidence_strength = evidence_data['overall_strength']
        evidence_score = evidence_data['total_score']
        
        # Map claim level to expected evidence score
        claim_expectations = {
            'Advanced': 70,
            'Intermediate': 40,
            'Basic': 20
        }
        
        expected_score = claim_expectations.get(claim_level, 40)
        
        # Calculate credibility score (0 to 1)
        if expected_score == 0:
            credibility_score = 1.0
        else:
            credibility_score = min(evidence_score / expected_score, 1.0)
        
        # Determine credibility category
        if credibility_score >= self.thresholds['HIGH']:
            category = 'Authentic'
            color = 'green'
        elif credibility_score >= self.thresholds['MEDIUM']:
            category = 'Partially Supported'
            color = 'orange'
        else:
            category = 'Likely Inflated'
            color = 'red'
        
        # Generate explanation
        explanation = self._generate_explanation(
            skill, claim_level, evidence_strength, 
            evidence_data, credibility_score
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            skill, claim_level, evidence_strength, credibility_score
        )
        
        return {
            'skill': skill,
            'claim_level': claim_level,
            'evidence_strength': evidence_strength,
            'credibility_score': round(credibility_score, 2),
            'credibility_category': category,
            'color': color,
            'explanation': explanation,
            'suggestions': suggestions,
            'evidence_details': evidence_data['details'][:5],
            'evidence_breakdown': evidence_data.get('breakdown', {})
        }
    
    def _generate_explanation(self, skill, claim_level, evidence_strength, 
                             evidence_data, score):
        """Generate human-readable explanation"""
        
        explanations = []
        
        # Main assessment
        if score >= 0.75:
            explanations.append(
                f"'{skill}' is claimed at {claim_level} level and strongly supported by evidence. "
                f"The evidence shows {evidence_strength.lower()} indicators across multiple sources."
            )
        elif score >= 0.40:
            explanations.append(
                f"'{skill}' is claimed at {claim_level} level with moderate evidence. "
                f"While some indicators are present, the evidence depth could be stronger."
            )
        else:
            explanations.append(
                f"'{skill}' is claimed at {claim_level} level but evidence is limited. "
                f"The claim may exceed demonstrated experience."
            )
        
        # Evidence breakdown
        breakdown = evidence_data.get('breakdown', {})
        strong_sources = [k for k, v in breakdown.items() if v == 'Strong']
        moderate_sources = [k for k, v in breakdown.items() if v == 'Moderate']
        weak_sources = [k for k, v in breakdown.items() if v in ['Weak', 'No Evidence']]
        
        if strong_sources:
            explanations.append(
                f"Strong evidence found in: {', '.join(strong_sources)}."
            )
        
        if moderate_sources:
            explanations.append(
                f"Moderate evidence found in: {', '.join(moderate_sources)}."
            )
        
        if weak_sources and len(weak_sources) == len(breakdown):
            explanations.append(
                "Limited concrete evidence across all sources."
            )
        
        return " ".join(explanations)
    
    def _generate_suggestions(self, skill, claim_level, evidence_strength, score):
        """Generate improvement suggestions"""
        
        suggestions = []
        
        if score < 0.40:
            suggestions.append(
                f"Build projects demonstrating practical {skill} skills"
            )
            suggestions.append(
                f"Document technical details, implementations, and outcomes"
            )
            suggestions.append(
                f"Consider earning certifications in {skill}"
            )
        elif score < 0.75:
            suggestions.append(
                f"Expand {skill} projects with more complexity"
            )
            suggestions.append(
                f"Add more detailed documentation and metrics"
            )
            suggestions.append(
                f"Contribute to open-source projects using {skill}"
            )
        else:
            suggestions.append(
                f"Excellent demonstration of {skill} - maintain this standard"
            )
            suggestions.append(
                f"Consider mentoring others or writing technical blogs about {skill}"
            )
        
        return suggestions[:3]  # Limit to top 3 suggestions
    
    def calculate_overall_credibility(self, skill_scores):
        """
        Calculate overall credibility score across all skills
        
        Args:
            skill_scores: list of individual skill score dicts
        
        Returns:
            dict with overall statistics
        """
        if not skill_scores:
            return {
                'overall_score': 0,
                'total_skills': 0,
                'authentic_count': 0,
                'partial_count': 0,
                'inflated_count': 0,
                'average_score': 0
            }
        
        total_skills = len(skill_scores)
        total_score = sum(s['credibility_score'] for s in skill_scores)
        average_score = total_score / total_skills
        
        # Count by category
        authentic_count = sum(1 for s in skill_scores if s['credibility_category'] == 'Authentic')
        partial_count = sum(1 for s in skill_scores if s['credibility_category'] == 'Partially Supported')
        inflated_count = sum(1 for s in skill_scores if s['credibility_category'] == 'Likely Inflated')
        
        return {
            'overall_score': round(average_score * 100, 1),
            'total_skills': total_skills,
            'authentic_count': authentic_count,
            'partial_count': partial_count,
            'inflated_count': inflated_count,
            'average_score': round(average_score, 2),
            'authentic_percentage': round((authentic_count / total_skills) * 100, 1),
            'partial_percentage': round((partial_count / total_skills) * 100, 1),
            'inflated_percentage': round((inflated_count / total_skills) * 100, 1)
        }
