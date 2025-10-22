from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.application import JobApplication
from app.models.user import User
from app.models.payment import Payment
from app import db
from app.services.ai_agent import AIAgentService
from app.services.job_scraper import JobScraperService
import json

applications_bp = Blueprint('applications', __name__)
ai_service = AIAgentService()
job_scraper = JobScraperService()

@applications_bp.route('/create', methods=['POST'])
@jwt_required()
def create_application():
    user_id = get_jwt_identity()
    
    # Check if user has active payment
    active_payment = Payment.query.filter_by(
        user_id=user_id, 
        status='completed'
    ).first()
    
    if not active_payment:
        return jsonify({'error': 'Payment required to access this service'}), 402
    
    data = request.get_json()
    
    application = JobApplication(
        user_id=user_id,
        original_resume=data.get('resume_text', ''),
        target_region=data.get('region'),
        target_town=data.get('town'),
        job_title=data.get('job_title'),
        industry=data.get('industry')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({
        'application_id': application.id,
        'message': 'Application created successfully'
    })

@applications_bp.route('/process/<application_id>', methods=['POST'])
@jwt_required()
def process_application(application_id):
    user_id = get_jwt_identity()
    
    application = JobApplication.query.filter_by(
        id=application_id, 
        user_id=user_id
    ).first()
    
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    try:
        # Step 1: Enhance resume with AI
        resume_result = ai_service.enhance_resume(
            application.original_resume,
            application.job_title,
            application.industry
        )
        
        if resume_result['success']:
            application.enhanced_resume = resume_result['enhanced_resume']
        
        # Step 2: Search for jobs
        search_keywords = application.job_title or ''
        jobs = job_scraper.search_jobs(
            keywords=search_keywords,
            region=application.target_region,
            town=application.target_town
        )
        
        application.set_job_matches(jobs)
        application.matches_found = len(jobs)
        application.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'application': application.to_dict(),
            'jobs_found': len(jobs)
        })
        
    except Exception as e:
        application.status = 'failed'
        db.session.commit()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@applications_bp.route('/history', methods=['GET'])
@jwt_required()
def application_history():
    user_id = get_jwt_identity()
    
    applications = JobApplication.query.filter_by(
        user_id=user_id
    ).order_by(JobApplication.created_at.desc()).all()
    
    return jsonify({
        'applications': [app.to_dict() for app in applications]
    })

@applications_bp.route('/regions', methods=['GET'])
def get_regions():
    """Get all South African regions and towns"""
    regions = {
        'gauteng': [
            'Johannesburg', 'Pretoria', 'Sandton', 'Randburg', 'Roodepoort',
            'Centurion', 'Midrand', 'Alberton', 'Kempton Park', 'Boksburg'
        ],
        'western_cape': [
            'Cape Town', 'Stellenbosch', 'Paarl', 'Wellington', 'George',
            'Mossel Bay', 'Worcester', 'Malmesbury'
        ],
        'eastern_cape': [
            'Port Elizabeth', 'East London', 'Grahamstown', 'Queenstown',
            'Bisho', 'Butterworth'
        ],
        'kwaZulu_natal': [
            'Durban', 'Pietermaritzburg', 'Richards Bay', 'Newcastle',
            'Ladysmith', 'Ballito', 'Umhlanga'
        ],
        'free_state': [
            'Bloemfontein', 'Welkom', 'Bethlehem', 'Kroonstad', 'Sasolburg'
        ],
        'limpopo': [
            'Polokwane', 'Lebowakgomo', 'Tzaneen', 'Phalaborwa', 'Modimolle'
        ],
        'mpumalanga': [
            'Nelspruit', 'Witbank', 'Middelburg', 'Standerton', 'Ermelo'
        ],
        'north_west': [
            'Rustenburg', 'Potchefstroom', 'Klerksdorp', 'Mahikeng', 'Zeerust'
        ],
        'northern_cape': [
            'Kimberley', 'Upington', 'Springbok', 'De Aar', 'Kuruman'
        ]
    }
    
    return jsonify(regions)
