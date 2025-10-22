import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List, Dict
import re

class JobScraperService:
    def __init__(self):
        self.south_africa_regions = {
            'gauteng': [
                'johannesburg', 'pretoria', 'sandton', 'randburg', 'roodepoort',
                'centurion', 'midrand', 'alberton', 'kempton-park', 'boksburg'
            ],
            'western_cape': [
                'cape-town', 'stellenbosch', 'paarl', 'wellington', 'george',
                'mossel-bay', 'worcester', 'malmesbury'
            ],
            'eastern_cape': [
                'port-elizabeth', 'east-london', 'grahamstown', 'queenstown',
                'bisho', 'butterworth'
            ],
            'kwaZulu_natal': [
                'durban', 'pietermaritzburg', 'richards-bay', 'newcastle',
                'ladysmith', 'ballito', 'umhlanga'
            ],
            'free_state': [
                'bloemfontein', 'welkom', 'bethlehem', 'kroonstad', 'sasolburg'
            ],
            'limpopo': [
                'polokwane', 'lebowakgomo', 'tzaneen', 'phalaborwa', 'modimolle'
            ],
            'mpumalanga': [
                'nelspruit', 'witbank', 'middelburg', 'standerton', 'ermelo'
            ],
            'north_west': [
                'rustenburg', 'potchefstroom', 'klerksdorp', 'mahikeng', 'zeerust'
            ],
            'northern_cape': [
                'kimberley', 'upington', 'springbok', 'de-aar', 'kuruman'
            ]
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
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_listings = soup.find_all('article', class_='job')
            
            for job in job_listings[:10]:  # Limit to 10 jobs
                try:
                    title_elem = job.find('h2')
                    company_elem = job.find('p', class_='company')
                    location_elem = job.find('ul', class_='location')
                    
                    if title_elem and company_elem:
                        job_data = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': base_url + title_elem.find('a')['href'] if title_elem.find('a') else '',
                            'source': 'careerjet'
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
                'l': location
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for job in job_cards[:10]:
                try:
                    title_elem = job.find('h2', class_='jobTitle')
                    company_elem = job.find('span', class_='companyName')
                    location_elem = job.find('div', class_='companyLocation')
                    
                    if title_elem and company_elem:
                        job_data = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': base_url + title_elem.find('a')['href'] if title_elem.find('a') else '',
                            'source': 'indeed'
                        }
                        jobs.append(job_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Indeed scraping error: {e}")
            
        return jobs
    
    def search_jobs(self, keywords: str, region: str, town: str = None) -> List[Dict]:
        """Main method to search jobs across multiple platforms"""
        all_jobs = []
        location = town if town else region
        
        # Search CareerJet
        careerjet_jobs = self.scrape_careerjet(keywords, location)
        all_jobs.extend(careerjet_jobs)
        
        # Search Indeed
        indeed_jobs = self.scrape_indeed(keywords, location)
        all_jobs.extend(indeed_jobs)
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            identifier = (job['title'], job['company'])
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs[:15]  # Return max 15 unique jobs
