import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List, Dict
import re
from datetime import datetime

class JobScraperService:
    def __init__(self):
        self.south_africa_regions = {
            'gauteng': [
                'johannesburg', 'pretoria', 'sandton', 'randburg', 'roodepoort',
                'centurion', 'midrand', 'alberton', 'kempton-park', 'boksburg',
                'benoni', 'springs', 'vereeniging', 'vanderbijlpark'
            ],
            'western_cape': [
                'cape-town', 'stellenbosch', 'paarl', 'wellington', 'george',
                'mossel-bay', 'worcester', 'malmesbury', 'bellville', 'parow',
                'somerset-west', 'constantia'
            ],
            'eastern_cape': [
                'port-elizabeth', 'east-london', 'grahamstown', 'queenstown',
                'bisho', 'butterworth', 'uitenhage', 'graaff-reinet'
            ],
            'kwaZulu_natal': [
                'durban', 'pietermaritzburg', 'richards-bay', 'newcastle',
                'ladysmith', 'ballito', 'umhlanga', 'pinetown', 'pmb'
            ],
            'free_state': [
                'bloemfontein', 'welkom', 'bethlehem', 'kroonstad', 'sasolburg',
                'phuthaditjhaba', 'botshabelo'
            ],
            'limpopo': [
                'polokwane', 'lebowakgomo', 'tzaneen', 'phalaborwa', 'modimolle',
                'bela-bela', 'mokopane'
            ],
            'mpumalanga': [
                'nelspruit', 'witbank', 'middelburg', 'standerton', 'ermelo',
                'bushbuckridge', 'mbombela'
            ],
            'north_west': [
                'rustenburg', 'potchefstroom', 'klerksdorp', 'mahikeng', 'zeerust',
                'lichtenburg', 'stilfontein'
            ],
            'northern_cape': [
                'kimberley', 'upington', 'springbok', 'de-aar', 'kuruman',
                'postmasburg', 'kathu'
            ]
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_careerjet(self, keywords: str, location: str) -> List[Dict]:
        """Scrape jobs from CareerJet South Africa"""
        jobs = []
        try:
            base_url = "https://www.careerjet.co.za"
            search_url = f"{base_url}/search/jobs"
            
            params = {
                's': keywords,
                'l': location,
                'radius': 25
            }
            
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_listings = soup.find_all('article', class_='job')
            
            for job in job_listings[:15]:
                try:
                    title_elem = job.find('h2')
                    company_elem = job.find('p', class_='company')
                    location_elem = job.find('ul', class_='location')
                    date_elem = job.find('span', class_='badge--default')
                    
                    if title_elem and company_elem:
                        job_data = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': base_url + title_elem.find('a')['href'] if title_elem.find('a') else '',
                            'source': 'careerjet',
                            'date_posted': date_elem.text.strip() if date_elem else 'Recent',
                            'salary': 'Not specified'
                        }
                        jobs.append(job_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"CareerJet scraping error: {e}")
            
        return jobs
    
    def scrape_indeed(self, keywords: str, location: str) -> List[Dict]:
        """Scrape jobs from Indeed South Africa"""
        jobs = []
        try:
            base_url = "https://za.indeed.com"
            search_url = f"{base_url}/jobs"
            
            params = {
                'q': keywords,
                'l': location,
                'fromage': 7  # Last 7 days
            }
            
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for job in job_cards[:15]:
                try:
                    title_elem = job.find('h2', class_='jobTitle')
                    company_elem = job.find('span', class_='companyName')
                    location_elem = job.find('div', class_='companyLocation')
                    salary_elem = job.find('div', class_='salary-snippet')
                    
                    if title_elem and company_elem:
                        job_data = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': base_url + title_elem.find('a')['href'] if title_elem.find('a') else '',
                            'source': 'indeed',
                            'date_posted': 'Recent',
                            'salary': salary_elem.text.strip() if salary_elem else 'Not specified'
                        }
                        jobs.append(job_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Indeed scraping error: {e}")
            
        return jobs
    
    def scrape_careers24(self, keywords: str, location: str) -> List[Dict]:
        """Scrape jobs from Careers24"""
        jobs = []
        try:
            base_url = "https://www.careers24.com"
            search_url = f"{base_url}/jobs"
            
            params = {
                'keywords': keywords,
                'location': location
            }
            
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_listings = soup.find_all('div', class_='job-card')
            
            for job in job_listings[:15]:
                try:
                    title_elem = job.find('h3')
                    company_elem = job.find('div', class_='company')
                    location_elem = job.find('div', class_='location')
                    
                    if title_elem and company_elem:
                        job_data = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': base_url + title_elem.find('a')['href'] if title_elem.find('a') else '',
                            'source': 'careers24',
                            'date_posted': 'Recent',
                            'salary': 'Not specified'
                        }
                        jobs.append(job_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Careers24 scraping error: {e}")
            
        return jobs
    
    def search_jobs(self, keywords: str, region: str, town: str = None) -> List[Dict]:
        """Main method to search jobs across multiple platforms"""
        all_jobs = []
        location = town if town else region
        
        print(f"Searching jobs for: {keywords} in {location}")
        
        # Search multiple platforms
        indeed_jobs = self.scrape_indeed(keywords, location)
        all_jobs.extend(indeed_jobs)
        
        careerjet_jobs = self.scrape_careerjet(keywords, location)
        all_jobs.extend(careerjet_jobs)
        
        careers24_jobs = self.scrape_careers24(keywords, location)
        all_jobs.extend(careers24_jobs)
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            identifier = (job['title'].lower(), job['company'].lower())
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        # Add timestamp
        for job in unique_jobs:
            job['scraped_at'] = datetime.utcnow().isoformat()
        
        return unique_jobs[:20]  # Return max 20 unique jobs
    
    def get_region_towns(self, region: str) -> List[str]:
        """Get towns for a specific region"""
        return self.south_africa_regions.get(region.lower(), [])
    
    def get_all_regions(self) -> Dict[str, List[str]]:
        """Get all regions and their towns"""
        return self.south_africa_regions
