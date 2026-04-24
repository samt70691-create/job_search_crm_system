from src.services.profile_service import load_profile
from src.utils.text import normalize_text


def compute_offer_score(job_type, has_contact=False, recent=False, attractive_salary=False, title='', description='', location=''):
    score = 0
    if job_type == 'CDI':
        score += 30
    elif job_type == 'alternance':
        score += 15
    if has_contact:
        score += 10
    if recent:
        score += 5
    if attractive_salary:
        score += 10

    profile = load_profile()
    text = normalize_text(' '.join([title or '', description or '', location or '']))
    keywords = [k.strip() for k in profile['priority_keywords'].split(',') if k.strip()]
    locations = [k.strip().lower() for k in profile['priority_locations'].split(',') if k.strip()]
    keyword_hits = sum(1 for kw in keywords if kw in text)
    score += min(keyword_hits * 4, 30)
    if any(loc in text for loc in locations):
        score += 10
    return min(score, 100)
