# Configuration file for Resume Skill Analyzer

# File upload restrictions
MAX_FILE_SIZE_MB = 5
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['pdf']

# Skill claim levels
CLAIM_LEVELS = {
    'ADVANCED': ['expert', 'advanced', 'proficient', 'mastery', 'experienced', 'specialized'],
    'INTERMEDIATE': ['intermediate', 'worked with', 'experience in', 'familiar', 'working knowledge'],
    'BASIC': ['basic', 'beginner', 'learning', 'exposure to', 'aware of', 'novice']
}

# Skill categories with keywords
SKILL_CATEGORIES = {
    'Programming Languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 
        'php', 'swift', 'kotlin', 'typescript', 'r', 'matlab', 'scala'
    ],
    'Web Development': [
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 
        'django', 'flask', 'fastapi', 'spring', 'asp.net', 'jquery'
    ],
    'Data Science & ML': [
        'machine learning', 'deep learning', 'ml', 'dl', 'ai', 'artificial intelligence',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas', 
        'numpy', 'matplotlib', 'seaborn', 'data analysis', 'statistics',
        'neural network', 'cnn', 'rnn', 'lstm', 'transformer', 'nlp', 
        'natural language processing', 'computer vision', 'opencv'
    ],
    'Databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 
        'oracle', 'sqlite', 'dynamodb', 'firebase'
    ],
    'Cloud & DevOps': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
        'terraform', 'ansible', 'git', 'github', 'gitlab', 'bitbucket'
    ],
    'Tools & Frameworks': [
        'git', 'linux', 'bash', 'vim', 'vscode', 'jupyter', 'anaconda',
        'postman', 'swagger', 'jira', 'agile', 'scrum'
    ]
}

# Evidence keywords for different skills
EVIDENCE_KEYWORDS = {
    'Deep Learning': {
        'models': ['cnn', 'rnn', 'lstm', 'gru', 'transformer', 'bert', 'gpt', 'resnet', 'vgg', 'inception'],
        'frameworks': ['tensorflow', 'pytorch', 'keras', 'jax', 'mxnet'],
        'metrics': ['accuracy', 'precision', 'recall', 'f1-score', 'loss', 'mse', 'mae', 'auc', 'roc'],
        'techniques': ['backpropagation', 'gradient descent', 'adam', 'sgd', 'batch normalization', 
                      'dropout', 'regularization', 'transfer learning', 'fine-tuning']
    },
    'Machine Learning': {
        'models': ['linear regression', 'logistic regression', 'decision tree', 'random forest', 
                  'svm', 'knn', 'naive bayes', 'xgboost', 'gradient boosting', 'clustering'],
        'frameworks': ['scikit-learn', 'sklearn', 'pandas', 'numpy'],
        'metrics': ['accuracy', 'precision', 'recall', 'f1-score', 'confusion matrix', 'cross-validation'],
        'techniques': ['feature engineering', 'feature selection', 'hyperparameter tuning', 
                      'train-test split', 'validation', 'overfitting', 'underfitting']
    },
    'Python': {
        'libraries': ['numpy', 'pandas', 'matplotlib', 'requests', 'flask', 'django', 'fastapi'],
        'concepts': ['oop', 'classes', 'functions', 'decorators', 'generators', 'list comprehension'],
        'tools': ['pip', 'virtualenv', 'conda', 'pytest', 'unittest']
    },
    'Data Analysis': {
        'libraries': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'scipy'],
        'techniques': ['data cleaning', 'data visualization', 'statistical analysis', 
                      'exploratory data analysis', 'eda', 'data preprocessing'],
        'tools': ['jupyter', 'excel', 'tableau', 'power bi']
    }
}

# Credibility score thresholds
SCORE_THRESHOLDS = {
    'HIGH': 0.75,      # Authentic
    'MEDIUM': 0.40,    # Partially supported
    'LOW': 0.0         # Likely inflated
}

# Resume section keywords
SECTION_KEYWORDS = {
    'skills': ['skills', 'technical skills', 'core competencies', 'expertise', 'technologies'],
    'projects': ['projects', 'project experience', 'academic projects', 'personal projects'],
    'experience': ['experience', 'work experience', 'employment', 'internship', 'work history'],
    'education': ['education', 'academic background', 'qualifications'],
    'certifications': ['certifications', 'certificates', 'licensed', 'accredited'],
    'achievements': ['achievements', 'accomplishments', 'awards', 'honors', 'recognition']
}

# GitHub analysis settings
GITHUB_ANALYSIS = {
    'max_repos': 10,
    'min_commits_active': 10,
    'complexity_threshold': 5
}
