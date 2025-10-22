from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_agent import AIAgentService
from app.services.document_processor import DocumentProcessor
import base64

ai_bp = Blueprint('ai_processing', __name__)
ai_service = AIAgentService()
doc_processor = DocumentProcessor()

@ai_bp.route('/enhance-resume', methods=['POST'])
@jwt_required()
def enhance_resume():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        resume_text = data.get('resume_text', '')
        job_title = data.get('job_title')
        industry = data.get('industry')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        result = ai_service.enhance_resume(resume_text, job_title, industry)
        
        if result['success']:
            return jsonify({
                'success': True,
                'enhanced_resume': result['enhanced_resume']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'AI processing failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/generate-cover-letter', methods=['POST'])
@jwt_required()
def generate_cover_letter():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        company = data.get('company')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400
        
        result = ai_service.generate_cover_letter(resume_text, job_description, company)
        
        if result['success']:
            return jsonify({
                'success': True,
                'cover_letter': result['cover_letter']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'AI processing failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/optimize-ats', methods=['POST'])
@jwt_required()
def optimize_ats():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        resume_text = data.get('resume_text', '')
        keywords = data.get('keywords', [])
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        if not isinstance(keywords, list):
            return jsonify({'error': 'Keywords must be a list'}), 400
        
        result = ai_service.optimize_for_ats(resume_text, keywords)
        
        if result['success']:
            return jsonify({
                'success': True,
                'optimized_resume': result['optimized_resume']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'AI processing failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/process-document', methods=['POST'])
@jwt_required()
def process_document():
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Extract text from document
        extracted_text = doc_processor.extract_text(file, file.filename)
        
        return jsonify({
            'success': True,
            'extracted_text': extracted_text,
            'filename': file.filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/analyze-job-description', methods=['POST'])
@jwt_required()
def analyze_job_description():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        job_description = data.get('job_description', '')
        resume_text = data.get('resume_text', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Use AI to analyze job description and provide insights
        prompt = f"""
        Analyze this job description and provide:
        1. Key skills and qualifications required
        2. Experience level
        3. Industry keywords
        4. Salary range estimation (if possible)
        5. Company culture insights
        
        Job Description:
        {job_description}
        
        Provide the analysis in a structured JSON format.
        """
        
        try:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a career advisor and job market analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )
            
            analysis = response.choices[0].message.content.strip()
            
            return jsonify({
                'success': True,
                'analysis': analysis
            })
            
        except Exception as ai_error:
            return jsonify({
                'success': False,
                'error': f'AI analysis failed: {str(ai_error)}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
