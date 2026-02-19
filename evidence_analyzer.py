"""
Evidence extraction and analysis from resume sections
"""
import re
from config import EVIDENCE_KEYWORDS


class EvidenceAnalyzer:
    def __init__(self):
        """Initialize evidence analyzer"""
        self.evidence_keywords = EVIDENCE_KEYWORDS
    
    def analyze_project_evidence(self, project_text, skill):
        """
        Analyze project text for evidence of a specific skill
        Returns evidence score and details
        """
        if not project_text:
            return {
                'score': 0,
                'strength': 'No Evidence',
                'details': []
            }
        
        text_lower = project_text.lower()
        skill_lower = skill.lower()
        
        evidence_details = []
        score = 0
        
        # Check if skill is mentioned
        if skill_lower in text_lower:
            score += 10
            evidence_details.append(f"Skill '{skill}' mentioned in projects")
        
        # Check for specific evidence keywords
        if skill in self.evidence_keywords:
            skill_evidence = self.evidence_keywords[skill]
            
            for evidence_type, keywords in skill_evidence.items():
                found_keywords = []
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        found_keywords.append(keyword)
                        score += 5
                
                if found_keywords:
                    evidence_details.append(f"{evidence_type.title()}: {', '.join(found_keywords[:3])}")
        
        # Check for technical depth indicators
        depth_indicators = [
            ('implementation', 5), ('developed', 5), ('built', 5), ('created', 5),
            ('designed', 5), ('architecture', 7), ('algorithm', 7), ('optimized', 7),
            ('deployed', 6), ('tested', 4), ('evaluated', 6), ('achieved', 6)
        ]
        
        for indicator, points in depth_indicators:
            if indicator in text_lower:
                score += points
                evidence_details.append(f"Action: {indicator}")
        
        # Determine evidence strength
        if score >= 50:
            strength = 'Strong'
        elif score >= 25:
            strength = 'Moderate'
        elif score > 0:
            strength = 'Weak'
        else:
            strength = 'No Evidence'
        
        return {
            'score': score,
            'strength': strength,
            'details': evidence_details[:5]  # Limit to top 5 details
        }
    
    def analyze_experience_evidence(self, experience_text, skill):
        """
        Analyze work experience for evidence of a specific skill
        Returns evidence score and details
        """
        if not experience_text:
            return {
                'score': 0,
                'strength': 'No Evidence',
                'details': []
            }
        
        text_lower = experience_text.lower()
        skill_lower = skill.lower()
        
        evidence_details = []
        score = 0
        
        # Check if skill is mentioned
        if skill_lower in text_lower:
            score += 15
            evidence_details.append(f"Used '{skill}' in professional work")
        
        # Check for professional experience indicators
        experience_indicators = [
            ('years', 10), ('months', 5), ('team', 8), ('led', 10),
            ('managed', 10), ('collaborated', 7), ('delivered', 8),
            ('production', 10), ('clients', 8), ('users', 7)
        ]
        
        for indicator, points in experience_indicators:
            if indicator in text_lower:
                score += points
                evidence_details.append(f"Professional context: {indicator}")
        
        # Determine evidence strength
        if score >= 40:
            strength = 'Strong'
        elif score >= 20:
            strength = 'Moderate'
        elif score > 0:
            strength = 'Weak'
        else:
            strength = 'No Evidence'
        
        return {
            'score': score,
            'strength': strength,
            'details': evidence_details[:5]
        }
    
    def analyze_certification_evidence(self, cert_text, skill):
        """
        Analyze certifications for evidence of a specific skill
        """
        if not cert_text:
            return {
                'score': 0,
                'strength': 'No Evidence',
                'details': []
            }
        
        text_lower = cert_text.lower()
        skill_lower = skill.lower()
        
        evidence_details = []
        score = 0
        
        # Check if skill is in certification
        if skill_lower in text_lower:
            score += 20
            evidence_details.append(f"Certified in '{skill}'")
        
        # Check for certification keywords
        cert_keywords = ['certified', 'certificate', 'certification', 'licensed', 'accredited']
        for keyword in cert_keywords:
            if keyword in text_lower:
                score += 10
                evidence_details.append(f"Formal certification: {keyword}")
                break
        
        # Determine evidence strength
        if score >= 30:
            strength = 'Strong'
        elif score >= 15:
            strength = 'Moderate'
        elif score > 0:
            strength = 'Weak'
        else:
            strength = 'No Evidence'
        
        return {
            'score': score,
            'strength': strength,
            'details': evidence_details
        }
    
    def combine_evidence(self, project_evidence, experience_evidence, cert_evidence):
        """
        Combine evidence from multiple sources
        Returns overall evidence assessment
        """
        total_score = (
            project_evidence['score'] + 
            experience_evidence['score'] + 
            cert_evidence['score']
        )
        
        all_details = []
        all_details.extend(project_evidence['details'])
        all_details.extend(experience_evidence['details'])
        all_details.extend(cert_evidence['details'])
        
        # Determine overall strength
        if total_score >= 70:
            overall_strength = 'Strong'
        elif total_score >= 35:
            overall_strength = 'Moderate'
        elif total_score > 0:
            overall_strength = 'Weak'
        else:
            overall_strength = 'No Evidence'
        
        return {
            'total_score': total_score,
            'overall_strength': overall_strength,
            'details': all_details,
            'breakdown': {
                'projects': project_evidence['strength'],
                'experience': experience_evidence['strength'],
                'certifications': cert_evidence['strength']
            }
        }
