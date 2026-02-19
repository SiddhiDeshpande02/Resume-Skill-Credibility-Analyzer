"""
Utility functions for text extraction and preprocessing
"""
import re
import pdfplumber
from PIL import Image
import pytesseract
from io import BytesIO


def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_image(file):
    """Extract text from image using OCR"""
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")


def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep essential punctuation
    text = re.sub(r'[^\w\s\-.,;:()\[\]{}]', '', text)
    return text.strip()


def segment_resume_sections(text):
    """
    Segment resume into different sections
    Returns a dictionary with section names as keys
    """
    from config import SECTION_KEYWORDS
    
    text_lower = text.lower()
    sections = {}
    
    # Find section positions
    section_positions = []
    for section_name, keywords in SECTION_KEYWORDS.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                section_positions.append({
                    'name': section_name,
                    'start': match.start(),
                    'keyword': keyword
                })
    
    # Sort by position
    section_positions.sort(key=lambda x: x['start'])
    
    # Extract content between sections
    for i, section in enumerate(section_positions):
        start = section['start']
        end = section_positions[i + 1]['start'] if i + 1 < len(section_positions) else len(text)
        
        section_text = text[start:end]
        section_name = section['name']
        
        if section_name in sections:
            sections[section_name] += "\n" + section_text
        else:
            sections[section_name] = section_text
    
    # If no sections found, treat entire text as skills section
    if not sections:
        sections['full_text'] = text
    
    return sections


def extract_urls_from_text(text):
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls


def extract_github_url(text):
    """Extract GitHub profile URL from text"""
    github_pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+'
    matches = re.findall(github_pattern, text)
    return matches[0] if matches else None


def get_file_size_mb(file):
    """Get file size in MB"""
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset position
    return size / (1024 * 1024)


def validate_file(file, allowed_extensions, max_size_mb):
    """
    Validate uploaded file
    Returns (is_valid, error_message)
    """
    # Check file size
    size_mb = get_file_size_mb(file)
    if size_mb > max_size_mb:
        return False, f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
    
    # Check extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return False, f"File type '.{file_extension}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    return True, None
