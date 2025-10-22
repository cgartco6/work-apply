import re
import string
from typing import Dict, Any
from datetime import datetime
import json

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate South African phone number format"""
    # South African phone numbers: +27 followed by 9 digits, or 0 followed by 9 digits
    pattern = r'^(\+27|0)[1-9][0-9]{8}$'
    return bool(re.match(pattern, phone.replace(' ', '')))

def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit")
    
    if not any(char in string.punctuation for char in password):
        errors.append("Password must contain at least one special character")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def format_currency(amount: float) -> str:
    """Format amount as South African Rand"""
    return f"R{amount:,.2f}"

def generate_reference(prefix: str = "REF") -> str:
    """Generate a unique reference number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{prefix}{timestamp}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove potentially dangerous characters"""
    # Keep only alphanumeric, dots, underscores, and hyphens
    filename = re.sub(r'[^\w\.\-]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    return filename

def format_date(date_string: str, format: str = "%Y-%m-%d") -> str:
    """Format date string"""
    try:
        if isinstance(date_string, str):
            # Try to parse various date formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
                try:
                    date_obj = datetime.strptime(date_string, fmt)
                    return date_obj.strftime(format)
                except ValueError:
                    continue
        return date_string
    except:
        return date_string

def calculate_readability_score(text: str) -> float:
    """Calculate simple readability score (0-100)"""
    try:
        sentences = text.split('.')
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple scoring algorithm
        score = 100 - (avg_sentence_length * 1.5 + avg_word_length * 10)
        return max(0, min(100, score))
    except:
        return 0

def is_valid_json(data: str) -> bool:
    """Check if string is valid JSON"""
    try:
        json.loads(data)
        return True
    except:
        return False

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           get_file_extension(filename) in allowed_extensions
