"""
PDF Report Generator for credibility analysis
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io


class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8
        ))
    
    def generate_report(self, analysis_results, user_type='Student'):
        """
        Generate PDF report
        
        Args:
            analysis_results: dict containing all analysis data
            user_type: 'Student' or 'HR'
        
        Returns:
            BytesIO buffer containing PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Title
        title_text = "Resume Skill Credibility Analysis Report"
        elements.append(Paragraph(title_text, self.styles['CustomTitle']))
        elements.append(Spacer(1, 12))
        
        # Report info
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(date_text, self.styles['CustomBody']))
        elements.append(Paragraph(f"Report Type: {user_type}", self.styles['CustomBody']))
        elements.append(Spacer(1, 20))
        
        # Overall Summary
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        overall_stats = analysis_results.get('overall_stats', {})
        
        summary_text = f"""
        This report analyzes the credibility of skills claimed in the resume against 
        demonstrated evidence from projects, experience, and certifications. 
        The analysis covers {overall_stats.get('total_skills', 0)} skills with an 
        overall credibility score of {overall_stats.get('overall_score', 0)}%.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 12))
        
        # Overall Statistics Table
        elements.append(Paragraph("Overall Statistics", self.styles['CustomSubHeading']))
        
        stats_data = [
            ['Metric', 'Value'],
            ['Total Skills Analyzed', str(overall_stats.get('total_skills', 0))],
            ['Overall Credibility Score', f"{overall_stats.get('overall_score', 0)}%"],
            ['Authentic Skills', f"{overall_stats.get('authentic_count', 0)} ({overall_stats.get('authentic_percentage', 0)}%)"],
            ['Partially Supported', f"{overall_stats.get('partial_count', 0)} ({overall_stats.get('partial_percentage', 0)}%)"],
            ['Likely Inflated', f"{overall_stats.get('inflated_count', 0)} ({overall_stats.get('inflated_percentage', 0)}%)"]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        # Individual Skill Analysis
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Skill Analysis", self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))
        
        skill_scores = analysis_results.get('skill_scores', [])
        
        for i, skill_data in enumerate(skill_scores):
            # Skill header
            skill_name = skill_data['skill']
            credibility_score = skill_data['credibility_score']
            category = skill_data['credibility_category']
            
            elements.append(Paragraph(
                f"{i+1}. {skill_name}", 
                self.styles['CustomSubHeading']
            ))
            
            # Skill details table
            skill_details = [
                ['Claim Level', skill_data['claim_level']],
                ['Evidence Strength', skill_data['evidence_strength']],
                ['Credibility Score', f"{credibility_score} ({category})"],
            ]
            
            skill_table = Table(skill_details, colWidths=[2*inch, 4*inch])
            skill_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            elements.append(skill_table)
            elements.append(Spacer(1, 8))
            
            # Explanation
            elements.append(Paragraph("<b>Analysis:</b>", self.styles['CustomBody']))
            elements.append(Paragraph(skill_data['explanation'], self.styles['CustomBody']))
            elements.append(Spacer(1, 8))
            
            # Suggestions (mainly for students)
            if user_type == 'Student':
                elements.append(Paragraph("<b>Improvement Suggestions:</b>", self.styles['CustomBody']))
                for suggestion in skill_data['suggestions']:
                    elements.append(Paragraph(f"• {suggestion}", self.styles['CustomBody']))
            
            elements.append(Spacer(1, 15))
            
            # Page break after every 2 skills for readability
            if (i + 1) % 2 == 0 and i < len(skill_scores) - 1:
                elements.append(PageBreak())
        
        # Recommendations section
        elements.append(PageBreak())
        elements.append(Paragraph("Recommendations", self.styles['CustomHeading']))
        
        if user_type == 'Student':
            recommendations = """
            Based on the analysis, here are key recommendations to improve your skill credibility:
            
            1. Focus on building substantial projects that demonstrate your claimed skills
            2. Document your work thoroughly with technical details and outcomes
            3. Contribute to open-source projects to gain real-world experience
            4. Earn relevant certifications to validate your knowledge
            5. Be honest about your skill level - it builds trust with recruiters
            6. Update your resume with quantifiable achievements and metrics
            """
        else:  # HR
            recommendations = """
            Based on the analysis, here are insights for the recruitment process:
            
            1. Skills with high credibility scores show strong evidence of practical experience
            2. Skills marked as "Partially Supported" may need further verification in interviews
            3. Skills with low credibility may indicate keyword stuffing or inflated claims
            4. Consider using technical assessments for skills with credibility concerns
            5. Look for candidates with consistent evidence across multiple sources
            6. This analysis should complement, not replace, human judgment in hiring
            """
        
        elements.append(Paragraph(recommendations, self.styles['CustomBody']))
        elements.append(Spacer(1, 12))
        
        # Footer
        elements.append(Spacer(1, 20))
        footer_text = """
        This report is generated by an AI-based Resume Skill Credibility Analyzer. 
        It is designed to help students improve their skills and assist recruiters in 
        making informed decisions. The analysis should be used as a guidance tool and 
        not as a sole decision-making factor.
        """
        elements.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
