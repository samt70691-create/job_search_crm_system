from src.services.profile_service import load_profile, save_profile
from src.db.repositories.jobs_repository import list_jobs, create_job
from src.db.repositories.contacts_repository import list_contacts, create_contact
from src.db.repositories.masters_repository import list_masters, create_master
from src.services.scoring_service import compute_offer_score


def ensure_bootstrap():
    profile = load_profile()
    save_profile(profile)
    if len(list_jobs(include_duplicates=True)) == 0:
        seed_jobs = [
            {
                'source': 'demo', 'source_job_id': 'demo-001', 'url': 'https://example.com/jobs/ai-engineer-health', 'title': 'AI Engineer - Health Data',
                'company': 'HealthTech Paris', 'location': 'Paris', 'job_type': 'CDI', 'description_raw': 'LLM RAG FastAPI Python SQL healthcare', 'description_clean': 'LLM RAG FastAPI Python SQL healthcare',
                'score': 88, 'status': 'to_apply', 'priority_level': 'high', 'keywords_detected': 'python,llm,rag,fastapi,sql,healthcare', 'notes': 'Très aligné avec ton CV.'
            },
            {
                'source': 'demo', 'source_job_id': 'demo-002', 'url': 'https://example.com/jobs/data-scientist-clinical', 'title': 'Data Scientist Clinique',
                'company': 'MedData Strasbourg', 'location': 'Strasbourg', 'job_type': 'CDI', 'description_raw': 'Python SQL séries temporelles données cliniques', 'description_clean': 'Python SQL séries temporelles données cliniques',
                'score': 84, 'status': 'new', 'priority_level': 'high', 'keywords_detected': 'python,sql,time series,clinical', 'notes': 'Très bonne proximité métier santé.'
            },
            {
                'source': 'demo', 'source_job_id': 'demo-003', 'url': 'https://example.com/jobs/llm-engineer-remote', 'title': 'LLM Engineer',
                'company': 'AI Studio Remote', 'location': 'Remote', 'job_type': 'CDI', 'description_raw': 'LangChain evaluation hallucination reduction prompt engineering', 'description_clean': 'LangChain evaluation hallucination reduction prompt engineering',
                'score': 91, 'status': 'to_apply', 'priority_level': 'high', 'keywords_detected': 'langchain,llm,evaluation,prompt engineering', 'notes': 'Très fort matching IA générative.'
            }
        ]
        for job in seed_jobs:
            create_job(job)
    if len(list_contacts()) == 0:
        create_contact({'company': 'HealthTech Paris', 'full_name': 'Camille Martin', 'role': 'Talent Acquisition', 'email': 'camille.martin@healthtech.example', 'contact_type': 'RH', 'confidence_score': 0.8, 'notes': 'Contact demo'})
    if len(list_masters()) == 0:
        create_master({'source': 'demo', 'url': 'https://example.com/master-ai-sante', 'program_name': 'Mastère IA Santé Avancée', 'institution': 'Institut Demo', 'city': 'Paris', 'domain': 'IA Santé', 'score': 76, 'description': 'Programme orienté IA appliquée en santé'})
