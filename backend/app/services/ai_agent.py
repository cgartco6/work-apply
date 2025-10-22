import openai
import os
from typing import Dict, List
import json

class AIAgentService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
    
    def enhance_resume(self, original_resume: str, job_title: str = None, industry: str = None) -> Dict:
        """Enhance and rewrite resume using AI"""
        
        prompt = f"""
        Please enhance and professionally rewrite the following resume. 
        Focus on:
        1. Improving action verbs and achievements
        2. Optimizing for ATS systems
        3. Adding quantifiable results
        4. Professional formatting
        5. Industry-specific keywords
        
        Original Resume:
        {original_resume}
        
        Target Industry: {industry if industry else 'General'}
        Target Job Title: {job_title if job_title else 'Various'}
        
        Return only the enhanced resume text without any explanations.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer and career coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            enhanced_resume = response.choices[0].message.content.strip()
            return {
                'success': True,
                'enhanced_resume': enhanced_resume
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_cover_letter(self, resume: str, job_description: str, company: str = None) -> Dict:
        """Generate personalized cover letter"""
        
        prompt = f"""
        Generate a professional cover letter based on the resume and job description.
        
        Resume:
        {resume}
        
        Job Description:
        {job_description}
        
        Company: {company if company else 'the company'}
        
        Return only the cover letter text without any explanations.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            cover_letter = response.choices[0].message.content.strip()
            return {
                'success': True,
                'cover_letter': cover_letter
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def optimize_for_ats(self, resume: str, keywords: List[str]) -> Dict:
        """Optimize resume for Applicant Tracking Systems"""
        
        keyword_str = ', '.join(keywords)
        
        prompt = f"""
        Optimize the following resume for Applicant Tracking Systems (ATS) by:
        1. Incorporating these keywords naturally: {keyword_str}
        2. Improving structure for ATS parsing
        3. Ensuring proper section headings
        4. Using standard job titles
        
        Resume to optimize:
        {resume}
        
        Return only the optimized resume text.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an ATS optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.5
            )
            
            optimized_resume = response.choices[0].message.content.strip()
            return {
                'success': True,
                'optimized_resume': optimized_resume
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
