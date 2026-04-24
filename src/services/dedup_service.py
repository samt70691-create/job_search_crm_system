from src.db.repositories.jobs_repository import list_jobs, mark_duplicate
from src.utils.text import similarity, normalize_text


def is_duplicate(existing_url, incoming_url):
    return bool(existing_url and incoming_url and existing_url.strip() == incoming_url.strip())


def detect_and_mark_duplicates():
    jobs = [dict(r) for r in list_jobs(include_duplicates=True)]
    marked = 0
    for i, ref in enumerate(jobs):
        for cand in jobs[i+1:]:
            if ref['id'] == cand['id']:
                continue
            same_company = normalize_text(ref.get('company')) == normalize_text(cand.get('company'))
            title_sim = similarity(ref.get('title', ''), cand.get('title', ''))
            loc_sim = similarity(ref.get('location', ''), cand.get('location', ''))
            if same_company and title_sim >= 0.88 and loc_sim >= 0.75:
                mark_duplicate(cand['id'], ref['id'])
                marked += 1
    return marked
