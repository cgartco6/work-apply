import openai
import os
from typing import Dict, List
import json

class AIAgentService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
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
        6. Clear section organization
        7. Professional summary
        8. Skills categorization
        
        Original Resume:
        {original_resume}
        
        Target Industry: {industry if industry else 'General'}
        Target Job Title: {job_title if job_title else 'Various'}
        
        Return only the enhanced resume text without any explanations or markdown formatting.
        Maintain the original structure but improve content and formatting.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer and career coach with expertise in ATS optimization."},
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
        Generate a professional, personalized cover letter based on the resume and job description.
        
        Requirements:
        1. Address it to the hiring manager
        2. Highlight relevant skills and experience from the resume
        3. Show enthusiasm for the specific role and company
        4. Professional tone but conversational
        5. 3-4 paragraphs maximum
        6. Include a call to action
        
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
                    {"role": "system", "content": "You are a professional cover letter writer who creates compelling, personalized cover letters."},
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
        3. Ensuring proper section headings (Experience, Education, Skills, etc.)
        4. Using standard job titles and section names
        5. Maintaining readability while optimizing for keywords
        6. Ensuring proper formatting that ATS systems can parse
        
        Resume to optimize:
        {resume}
        
        Return only the optimized resume text without explanations.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an ATS optimization expert who understands how recruiters and automated systems scan resumes."},
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
    
    def generate_follow_up_email(self, company: str, position: str, interview_date: str = None) -> Dict:
        """Generate follow-up email after application"""
        
        prompt = f"""
        Generate a professional follow-up email for a job application.
        
        Company: {company}
        Position: {position}
        Interview Date: {interview_date if interview_date else 'Not specified'}
        
        Requirements:
        1. Professional but friendly tone
        2. Reiterate interest in position
        3. Reference specific skills or experience
        4. Thank them for consideration
        5. Appropriate length (3-4 paragraphs)
        
        Return only the email text without subject line or explanations.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional career coach helping with job application follow-ups."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            follow_up_email = response.choices[0].message.content.strip()
            return {
                'success': True,
                'follow_up_email': follow_up_email
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
