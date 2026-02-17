import requests
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
import pytz

class JobService:
    API_URL = "https://jsearch.p.rapidapi.com/search"
    HEADERS = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    @staticmethod
    def search_jobs(query, location, date_posted='today', remote_only=False, num_pages=1, user_is_pro=False):
        cache_key = f"jobs_{query}_{location}_{date_posted}_{remote_only}_{num_pages}_{user_is_pro}"
        cached_results = cache.get(cache_key)
        
        if cached_results:
            return cached_results

        api_date_posted = date_posted
        if date_posted in ['1h', '8h']:
            api_date_posted = 'today'

        querystring = {
            "query": f"{query} in {location}",
            "page": "1",
            "num_pages": str(num_pages),
            "date_posted": api_date_posted,
            "remote_jobs_only": "true" if remote_only else "false"
        }

        try:
            response = requests.get(JobService.API_URL, headers=JobService.HEADERS, params=querystring)
            response.raise_for_status()
            data = response.json()
            jobs = data.get('data', [])

            # Filter for 1h and 8h if requested (Pro feature)
            if date_posted in ['1h', '8h'] and user_is_pro:
                hours = 1 if date_posted == '1h' else 8
                threshold = datetime.now(pytz.UTC) - timedelta(hours=hours)
                
                filtered_jobs = []
                for job in jobs:
                    # JSearch typically provides job_posted_at_datetime_utc
                    posted_at_str = job.get('job_posted_at_datetime_utc')
                    if posted_at_str:
                        posted_at = datetime.fromisoformat(posted_at_str.replace('Z', '+00:00'))
                        if posted_at >= threshold:
                            filtered_jobs.append(job)
                jobs = filtered_jobs

            # Limit results for free users
            if not user_is_pro:
                jobs = jobs[:10]

            cache.set(cache_key, jobs, 1800)  # Cache for 30 minutes
            return jobs
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return []
