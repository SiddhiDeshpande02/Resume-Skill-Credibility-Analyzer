"""
Skill extraction using NLP and pattern matching
"""
import re
import spacy
from config import SKILL_CATEGORIES, CLAIM_LEVELS


class SkillExtractor:
    def __init__(self):
        """Initialize skill extractor with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # If model not found, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Build comprehensive skill list
        self.all_skills = []
        for category, skills in SKILL_CATEGORIES.items():
            self.all_skills.extend(skills)
        
    def extract_skills_from_text(self, text):
        """
        Extract skills from text with claim levels
        Returns list of dicts: [{'skill': 'Python', 'claim_level': 'Advanced', 'context': '...'}]
        """
        text_lower = text.lower()
        extracted_skills = []
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract skills with context
        for skill in self.all_skills:
            skill_lower = skill.lower()
            
            # Find all occurrences of the skill
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                # Get context around the skill (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Detect claim level
                claim_level = self._detect_claim_level(context)
                
                # Add to extracted skills if not already present
                skill_exists = any(s['skill'].lower() == skill_lower for s in extracted_skills)
                if not skill_exists:
                    extracted_skills.append({
                        'skill': skill.title(),
                        'claim_level': claim_level,
                        'context': context.strip()
                    })
        
        return extracted_skills
    
    def _detect_claim_level(self, context):
        """
        Detect claim level from context
        Returns: 'Advanced', 'Intermediate', or 'Basic'
        """
        context_lower = context.lower()
        
        # Check for advanced keywords
        for keyword in CLAIM_LEVELS['ADVANCED']:
            if keyword in context_lower:
                return 'Advanced'
        
        # Check for intermediate keywords
        for keyword in CLAIM_LEVELS['INTERMEDIATE']:
            if keyword in context_lower:
                return 'Intermediate'
        
        # Check for basic keywords
        for keyword in CLAIM_LEVELS['BASIC']:
            if keyword in context_lower:
                return 'Basic'
        
        # Default to Intermediate if no explicit level found
        return 'Intermediate'
    
    def categorize_skills(self, skills):
        """
        Categorize skills into different categories
        Returns dict with categories as keys
        """
        categorized = {category: [] for category in SKILL_CATEGORIES.keys()}
        categorized['Other'] = []
        
        for skill_data in skills:
            skill_lower = skill_data['skill'].lower()
            found = False
            
            for category, category_skills in SKILL_CATEGORIES.items():
                if skill_lower in [s.lower() for s in category_skills]:
                    categorized[category].append(skill_data)
                    found = True
                    break
            
            if not found:
                categorized['Other'].append(skill_data)
        
        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}
        
        return categorized
    
    def extract_skills_from_sections(self, sections):
        """
        Extract skills from resume sections
        Returns dict with section-wise skills
        """
        section_skills = {}
        
        for section_name, section_text in sections.items():
            skills = self.extract_skills_from_text(section_text)
            if skills:
                section_skills[section_name] = skills
        
        return section_skills
