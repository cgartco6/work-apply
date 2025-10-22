import PyPDF2
import docx
import re
from typing import Optional

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX extraction error: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file) -> str:
        """Extract text from TXT file"""
        try:
            text = file.read().decode('utf-8')
            return text.strip()
        except Exception as e:
            raise Exception(f"TXT extraction error: {str(e)}")
    
    def extract_text(self, file, filename: str) -> str:
        """Extract text from various document formats"""
        
        if filename.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file)
        elif filename.lower().endswith('.docx'):
            return self.extract_text_from_docx(file)
        elif filename.lower().endswith('.doc'):
            return self.extract_text_from_docx(file)  # Try docx reader for .doc files
        elif filename.lower().endswith('.txt'):
            return self.extract_text_from_txt(file)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
    
    def clean_resume_text(self, text: str) -> str:
        """Clean and normalize resume text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\+\@\(\)]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def detect_sections(self, text: str) -> Dict[str, str]:
        """Detect and extract resume sections"""
        sections = {
            'contact': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': ''
        }
        
        # Common section headers
        section_patterns = {
            'contact': r'(contact|personal|details|information)',
            'summary': r'(summary|objective|profile|about)',
            'experience': r'(experience|work\s+history|employment|work)',
            'education': r'(education|qualifications|academic)',
            'skills': r'(skills|technical\s+skills|competencies)',
            'projects': r'(projects|portfolio|achievements)'
        }
        
        lines = text.split('\n')
        current_section = 'unknown'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    current_section = section
                    break
            else:
                # If not a header, add to current section
                if current_section in sections:
                    sections[current_section] += line + '\n'
        
        # Clean up sections
        for key in sections:
            sections[key] = sections[key].strip()
        
        return sections
    
    def parse_resume(self, file, filename: str) -> Dict:
        """Parse resume and extract structured information"""
        try:
            # Extract raw text
            raw_text = self.extract_text(file, filename)
            
            # Clean text
            clean_text = self.clean_resume_text(raw_text)
            
            # Detect sections
            sections = self.detect_sections(clean_text)
            
            return {
                'success': True,
                'raw_text': raw_text,
                'clean_text': clean_text,
                'sections': sections,
                'word_count': len(clean_text.split()),
                'character_count': len(clean_text)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
