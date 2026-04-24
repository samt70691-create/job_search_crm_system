from src.ai.gemini_client import gemini_extract
from src.db.repositories.jobs_repository import get_job, update_job


def enrich_job_with_ai(job_id):
    job = get_job(job_id)
    if not job:
        return False
    result = gemini_extract((job['description_clean'] or '')[:12000])
    update_job(job_id, {
        'title': job['title'],
        'company': job['company'],
        'location': job['location'],
        'job_type': job['job_type'],
        'url': job['url'],
        'score': job['score'],
        'priority_level': result.get('priority_level') or job['priority_level'],
        'status': job['status'],
        'notes': job['notes']
    })
    return result
