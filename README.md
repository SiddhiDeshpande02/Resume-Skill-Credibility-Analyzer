# Resume Skill Credibility Analyzer

An AI-powered system to detect fake skill inflation in student resumes by comparing claimed skills against demonstrated evidence from projects, experience, and GitHub profiles.

## Features

- **Smart Skill Extraction**: Uses NLP (spaCy) to dynamically extract skills from resumes
- **Evidence Analysis**: Analyzes projects, work experience, certifications, and achievements
- **GitHub Integration**: Optional GitHub profile analysis for additional verification
- **Credibility Scoring**: Assigns credibility scores (0-1) to each skill based on evidence
- **Detailed Explanations**: Provides clear reasoning for each score
- **Interactive Dashboard**: Beautiful Streamlit interface with charts and visualizations
- **PDF Reports**: Generate downloadable PDF reports with complete analysis
- **Dual User Modes**: 
  - **Student Mode**: Get improvement suggestions and skill gap insights
  - **HR Mode**: Get hiring insights and credibility assessment

## System Architecture

```
Resume Upload (PDF/Image)
      ↓
Text Extraction (pdfplumber/OCR)
      ↓
Section Segmentation (Projects, Experience, etc.)
      ↓
Skill Extraction (NLP with spaCy)
      ↓
Evidence Extraction (Projects, Experience, Certifications)
      ↓
GitHub Analysis (Optional)
      ↓
Skill-Evidence Mapping
      ↓
Credibility Scoring
      ↓
Visualization & Reporting
```

## File Structure

```
resume_skill_analyzer/
│
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and constants
├── utils.py                    # Utility functions (text extraction, validation)
├── skill_extractor.py          # NLP-based skill extraction
├── evidence_analyzer.py        # Evidence extraction and analysis
├── github_analyzer.py          # GitHub profile analysis
├── credibility_scorer.py       # Credibility scoring engine
├── report_generator.py         # PDF report generation
├── requirements.txt            # Python dependencies
├── setup.sh                    # Installation script
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (for image-based resume extraction)

### Quick Setup

1. **Clone or download the project**
   ```bash
   cd resume_skill_analyzer
   ```

2. **Run the setup script** (Linux/Mac)
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Manual setup** (All platforms)
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Download spaCy model
   python -m spacy download en_core_web_sm
   ```

4. **Install Tesseract OCR** (for image resume support)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   ```
   
   **MacOS:**
   ```bash
   brew install tesseract
   ```
   
   **Windows:**
   Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Running the Application

1. **Activate virtual environment** (if not already activated)
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser**
   The app will automatically open at `http://localhost:8501`

### Using the Application

1. **Select User Type**: Choose Student or HR/Recruiter mode
2. **Upload Resume**: Upload PDF or image (JPG, PNG) - max 5MB
3. **Add GitHub** (Optional): Paste your GitHub profile URL for additional analysis
4. **Analyze**: Click "Analyze Resume" and wait for processing
5. **View Results**: Check the "Results & Report" tab for:
   - Overall credibility score
   - Individual skill scores
   - Detailed explanations
   - Evidence breakdown
   - Improvement suggestions (Student mode)
6. **Download Report**: Generate and download a comprehensive PDF report

## How It Works

### 1. Skill Extraction
- Uses spaCy NLP to extract skills from resume text
- Detects claim levels (Advanced, Intermediate, Basic)
- Categorizes skills (Programming, Web Dev, ML, etc.)

### 2. Evidence Analysis
The system looks for evidence in:
- **Projects**: Technical depth, libraries used, problem complexity
- **Experience**: Professional usage, team context, deliverables
- **Certifications**: Formal validation of skills
- **GitHub**: Code quality, activity level, language diversity

### 3. Credibility Scoring

**Score Calculation:**
```
credibility_score = evidence_score / expected_score
```

**Score Categories:**
- **≥ 0.75**: Authentic (Strong evidence)
- **0.40 - 0.74**: Partially Supported (Moderate evidence)
- **< 0.40**: Likely Inflated (Weak evidence)

### 4. Evidence Strength Assessment

**Strong Evidence Indicators:**
- Multiple implementations
- Technical documentation
- Evaluation metrics
- Professional usage
- GitHub activity

**Weak Evidence Indicators:**
- Only keyword mentions
- No technical details
- No practical application
- No measurable outcomes

## UI/UX Features

- **Clean Modern Design**: White background with dark accents
- **Color-Coded Results**: 
  - Green: Authentic skills
  - Yellow: Partially supported
  - Red: Likely inflated
- **Interactive Charts**: Pie charts, bar graphs, and distribution plots
- **Expandable Details**: Click to see detailed analysis per skill
- **Responsive Layout**: Works on desktop and tablet screens

## Configuration

Edit `config.py` to customise:

- **File size limits**: `MAX_FILE_SIZE_MB = 5`
- **Skill categories**: Add or modify skill lists
- **Evidence keywords**: Customize evidence detection
- **Score thresholds**: Adjust credibility ranges
- **GitHub settings**: Max repos analyzed

## Example Output

```
Overall Credibility Score: 72.5%
Total Skills Analyzed: 8

Skill Breakdown:
Python (Advanced) - Score: 0.85 - Authentic
   Evidence: Found in 3 projects, GitHub repos, professional experience
   
Deep Learning (Advanced) - Score: 0.45 - Partially Supported
   Evidence: Basic implementations, limited evaluation metrics
   Suggestion: Build more complex models with proper evaluation
   
React (Expert) - Score: 0.25 - Likely Inflated
   Evidence: Only keyword mentions, no projects or GitHub evidence
   Suggestion: Create React projects and document implementation
```

## Ethics & Safety

This system is designed with ethical principles:

- **Assistive, not punitive**: Helps students improve, doesn't reject them
- **Explainable**: Every score comes with clear reasoning
- **No labeling**: Doesn't call students "liars"
- **Opt-in**: Students choose to use it
- **Improvement-focused**: Provides actionable suggestions
- **Confidence ranges**: Acknowledges uncertainty

## Limitations

- Works best with English resumes
- Requires clearly structured resume sections
- GitHub analysis needs public repositories
- May not capture all evidence formats
- Scoring is heuristic-based, not perfect

## Future Enhancements

- [ ] Support for more languages
- [ ] LinkedIn profile integration
- [ ] LeetCode/Competitive programming analysis
- [ ] Course certificate verification
- [ ] Machine learning for improved scoring
- [ ] Batch resume processing for recruiters
- [ ] Resume improvement recommendations
- [ ] Skills market demand analysis

## Troubleshooting

### Common Issues

**Issue**: "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

**Issue**: "Tesseract not found" (for image resumes)
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
brew install tesseract              # MacOS
```

**Issue**: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: "GitHub API rate limit"
- Wait 60 minutes or use without GitHub analysis
- GitHub API allows 60 requests per hour for unauthenticated users

## License

This project is for educational and research purposes.

## Contributing

Contributions are welcome! Areas to improve:
- Better evidence detection algorithms
- More skill categories and keywords
- Improved UI/UX
- Additional data sources (LinkedIn, etc.)
- Multilingual support

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Built using Python, Streamlit, spaCy, and modern NLP techniques**
