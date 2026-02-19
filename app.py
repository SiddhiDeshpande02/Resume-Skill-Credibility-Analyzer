"""
Resume Skill Credibility Analyzer - Streamlit App
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Import custom modules
from utils import (
    extract_text_from_pdf, segment_resume_sections, extract_github_url, validate_file
)
from config import (
    MAX_FILE_SIZE_MB, ALLOWED_IMAGE_EXTENSIONS, 
    ALLOWED_DOCUMENT_EXTENSIONS
)
from skill_extractor import SkillExtractor
from evidence_analyzer import EvidenceAnalyzer
from github_analyzer import GitHubAnalyzer
from credibility_scorer import CredibilityScorer
from report_generator import ReportGenerator


# Page configuration
st.set_page_config(
    page_title="Resume Skill Credibility Analyzer",
    page_icon="**",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #34495e;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #2c3e50;
        margin: 10px 0;
    }
    .skill-authentic {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .skill-partial {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .skill-inflated {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    h1 {
        color: #1a1a1a;
        font-weight: 700;
    }
    h2, h3 {
        color: #2c3e50;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("Resume Skill Credibility Analyzer")
    st.markdown('<p class="subtitle">AI-powered system to detect skill inflation and help students improve</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # User type selection
        user_type = st.radio(
            "Select User Type:",
            ["Student", "HR/Recruiter"],
            help="Students get improvement suggestions, HR gets hiring insights"
        )
        
        st.markdown("---")
        
        st.subheader("About")
        st.info(
            """
            This system analyzes your resume to:
            - Extract claimed skills
            - Find evidence in projects & experience
            - Calculate credibility scores
            - Provide actionable feedback
            
            **Note:** This is an assistive tool, not a judgment system.
            """
        )
        
        st.markdown("---")
        st.caption("Built using Streamlit")
    
    # Main content area
    tab1, tab2 = st.tabs(["Upload & Analyze", "Results & Report"])
    
    with tab1:
        upload_and_analyze_section(user_type)
    
    with tab2:
        if st.session_state.analysis_complete:
            display_results_section(user_type)
        else:
            st.info("Please upload and analyze a resume first to see results here.")


def upload_and_analyze_section(user_type):
    """Handle file upload and analysis"""
    st.header("Upload Resume")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF or Image)",
            type=ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS,
            help=f"Max file size: {MAX_FILE_SIZE_MB}MB. Supported formats: PDF, JPG, PNG"
        )
    
    with col2:
        st.markdown("###Requirements")
        st.markdown(f"""
        - Max size: **{MAX_FILE_SIZE_MB}MB**
        - Formats: **PDF, JPG, PNG**
        - Clear & readable text
        """)
    
    # GitHub URL (optional)
    st.markdown("---")
    st.subheader("GitHub Profile (Optional)")
    github_url = st.text_input(
        "GitHub Profile URL",
        placeholder="https://github.com/username",
        help="Optional: Add your GitHub profile for additional analysis"
    )
    
    # Analyze button
    st.markdown("---")
    if st.button("Analyze Resume", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Please upload a resume file first!")
            return
        
        # Validate file
        all_extensions = ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS
        is_valid, error_msg = validate_file(uploaded_file, all_extensions, MAX_FILE_SIZE_MB)
        
        if not is_valid:
            st.error(f"{error_msg}")
            return
        
        # Start analysis
        with st.spinner("Analyzing your resume... This may take a minute..."):
            try:
                results = perform_analysis(uploaded_file, github_url)
                st.session_state.analysis_results = results
                st.session_state.analysis_complete = True
                st.success("Analysis complete! Check the 'Results & Report' tab.")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.exception(e)


def perform_analysis(uploaded_file, github_url=None):
    """Perform complete resume analysis"""
    
    # Step 1: Extract text
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Extracting text from resume...")
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        "display that this is not a pdf file"          
    
    progress_bar.progress(20)
    
    # Step 2: Segment sections
    status_text.text("Segmenting resume sections...")
    sections = segment_resume_sections(resume_text)
    progress_bar.progress(30)
    
    # Step 3: Extract skills
    status_text.text("Extracting skills...")
    skill_extractor = SkillExtractor()
    
    # Extract from all sections
    all_skills = []
    for section_name, section_text in sections.items():
        skills = skill_extractor.extract_skills_from_text(section_text)
        all_skills.extend(skills)
    
    # Remove duplicates (keep first occurrence)
    seen_skills = set()
    unique_skills = []
    for skill in all_skills:
        if skill['skill'].lower() not in seen_skills:
            seen_skills.add(skill['skill'].lower())
            unique_skills.append(skill)
    
    progress_bar.progress(45)
    
    # Step 4: Extract evidence
    status_text.text("Analyzing evidence...")
    evidence_analyzer = EvidenceAnalyzer()
    
    # Get relevant sections for evidence
    projects_text = sections.get('projects', '') + sections.get('full_text', '')
    experience_text = sections.get('experience', '') + sections.get('full_text', '')
    cert_text = sections.get('certifications', '') + sections.get('achievements', '')
    
    progress_bar.progress(60)
    
    # Step 5: GitHub analysis (if provided)
    github_analysis = None
    github_skills = []
    
    if github_url and github_url.strip():
        status_text.text("Analyzing GitHub profile...")
        github_analyzer = GitHubAnalyzer()
        github_analysis = github_analyzer.analyze_profile(github_url.strip())
        
        if github_analysis:
            github_skills = github_analyzer.extract_skills_from_github(github_analysis)
    
    progress_bar.progress(75)
    
    # Step 6: Calculate credibility scores
    status_text.text("Calculating credibility scores...")
    scorer = CredibilityScorer()
    
    skill_scores = []
    for skill_data in unique_skills:
        skill = skill_data['skill']
        
        # Analyze evidence from different sources
        project_evidence = evidence_analyzer.analyze_project_evidence(projects_text, skill)
        experience_evidence = evidence_analyzer.analyze_experience_evidence(experience_text, skill)
        cert_evidence = evidence_analyzer.analyze_certification_evidence(cert_text, skill)
        
        # Check GitHub evidence
        github_boost = 0
        for gh_skill in github_skills:
            if gh_skill['skill'].lower() == skill.lower():
                github_boost = 15
                project_evidence['score'] += github_boost
                project_evidence['details'].append(f"Found in GitHub: {gh_skill['evidence']}")
                break
        
        # Combine evidence
        combined_evidence = evidence_analyzer.combine_evidence(
            project_evidence, experience_evidence, cert_evidence
        )
        
        # Calculate score
        score_result = scorer.calculate_skill_score(skill_data, combined_evidence)
        skill_scores.append(score_result)
    
    progress_bar.progress(90)
    
    # Step 7: Calculate overall statistics
    status_text.text("Generating statistics...")
    overall_stats = scorer.calculate_overall_credibility(skill_scores)
    
    progress_bar.progress(100)
    status_text.text("Analysis complete!")
    
    # Compile results
    results = {
        'skill_scores': skill_scores,
        'overall_stats': overall_stats,
        'github_analysis': github_analysis,
        'total_skills': len(skill_scores),
        'sections_found': list(sections.keys()),
        'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return results


def display_results_section(user_type):
    """Display analysis results"""
    results = st.session_state.analysis_results
    
    if not results:
        st.warning("No analysis results available.")
        return
    
    # Overall Statistics
    st.header("Overall Credibility Analysis")
    
    overall_stats = results['overall_stats']
    
    # Metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{overall_stats['overall_score']}%",
            help="Average credibility across all skills"
        )
    
    with col2:
        st.metric(
            "Total Skills",
            overall_stats['total_skills'],
            help="Number of skills analyzed"
        )
    
    with col3:
        st.metric(
            "Authentic",
            f"{overall_stats['authentic_count']} ({overall_stats['authentic_percentage']}%)",
            help="Skills with strong evidence"
        )
    
    with col4:
        st.metric(
            "Need Improvement",
            f"{overall_stats['inflated_count']} ({overall_stats['inflated_percentage']}%)",
            help="Skills that need more evidence"
        )
    
    # Visualization
    st.markdown("---")
    st.subheader("Credibility Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Authentic', 'Partially Supported', 'Likely Inflated'],
            values=[
                overall_stats['authentic_count'],
                overall_stats['partial_count'],
                overall_stats['inflated_count']
            ],
            marker=dict(colors=['#28a745', '#ffc107', '#dc3545']),
            hole=0.4
        )])
        fig_pie.update_layout(
            title="Skills by Credibility Category",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart of individual skills
        skill_scores = results['skill_scores']
        df = pd.DataFrame([
            {
                'Skill': s['skill'],
                'Score': s['credibility_score'] * 100,
                'Category': s['credibility_category']
            }
            for s in skill_scores
        ])
        
        fig_bar = px.bar(
            df,
            x='Score',
            y='Skill',
            color='Category',
            orientation='h',
            color_discrete_map={
                'Authentic': '#28a745',
                'Partially Supported': '#ffc107',
                'Likely Inflated': '#dc3545'
            },
            title="Individual Skill Scores"
        )
        fig_bar.update_layout(height=400, xaxis_title="Credibility Score (%)")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed Skill Analysis
    st.markdown("---")
    st.subheader("Detailed Skill Analysis")
    
    # Filter options
    filter_option = st.selectbox(
        "Filter by category:",
        ["All Skills", "Authentic", "Partially Supported", "Likely Inflated"]
    )
    
    # Filter skills
    if filter_option != "All Skills":
        filtered_skills = [s for s in skill_scores if s['credibility_category'] == filter_option]
    else:
        filtered_skills = skill_scores
    
    # Display each skill
    for i, skill_data in enumerate(filtered_skills):
        category = skill_data['credibility_category']
        
        if category == 'Authentic':
            css_class = 'skill-authentic'
        elif category == 'Partially Supported':
            css_class = 'skill-partial'
        else:
            css_class = 'skill-inflated'
        
        with st.container():
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {skill_data['skill']}")
            
            with col2:
                st.metric("Score", f"{skill_data['credibility_score'] * 100:.0f}%")
            
            # Details
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Claim Level:** {skill_data['claim_level']}")
            with col2:
                st.markdown(f"**Evidence:** {skill_data['evidence_strength']}")
            with col3:
                st.markdown(f"**Status:** {skill_data['credibility_category']}")
            
            # Explanation
            with st.expander("See detailed analysis"):
                st.markdown("**Analysis:**")
                st.write(skill_data['explanation'])
                
                if skill_data['evidence_details']:
                    st.markdown("**Evidence Found:**")
                    for detail in skill_data['evidence_details']:
                        st.write(f"- {detail}")
                
                # Suggestions (for students)
                if user_type == "Student":
                    st.markdown("**Improvement Suggestions:**")
                    for suggestion in skill_data['suggestions']:
                        st.write(f"• {suggestion}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("")
    
    # GitHub Analysis (if available)
    if results.get('github_analysis'):
        st.markdown("---")
        st.subheader("GitHub Analysis")
        
        github_data = results['github_analysis']
        repo_analysis = github_data.get('repository_analysis', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Public Repos", github_data.get('public_repos', 0))
        with col2:
            st.metric("Total Stars", repo_analysis.get('total_stars', 0))
        with col3:
            st.metric("Activity Level", repo_analysis.get('activity_level', 'N/A'))
        
        # Languages
        if repo_analysis.get('languages'):
            st.markdown("**Top Languages:**")
            langs = repo_analysis['languages']
            st.write(", ".join([f"{k} ({v})" for k, v in langs.items()]))
    
    # Download Report
    st.markdown("---")
    st.subheader("Download Report")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(
            "Download a comprehensive PDF report with all analysis details, "
            "explanations, and recommendations."
        )
    
    with col2:
        if st.button("Generate PDF Report", use_container_width=True):
            with st.spinner("Generating report..."):
                try:
                    report_gen = ReportGenerator()
                    pdf_buffer = report_gen.generate_report(results, user_type)
                    
                    st.download_button(
                        label="⬇Download PDF",
                        data=pdf_buffer,
                        file_name=f"skill_credibility_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("Report generated successfully!")
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    main()
