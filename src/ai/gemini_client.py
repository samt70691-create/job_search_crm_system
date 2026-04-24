import os
import json
import urllib.request


def gemini_extract(job_text: str):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {'summary': None, 'fit_reason': None, 'key_skills': [], 'seniority': None, 'priority_level': None}
    return {'summary': 'IA non activée dans cette sandbox', 'fit_reason': None, 'key_skills': [], 'seniority': None, 'priority_level': None}
