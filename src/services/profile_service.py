from src.db.repositories.settings_repository import get_setting, set_setting

DEFAULT_PROFILE = {
    'candidate_name': 'Yamina Sadallah',
    'headline': 'AI Engineer · Data & Intelligence Artificielle',
    'email': 'sadallah.yr@gmail.com',
    'phone': '+33 07 67 98 93 69',
    'location': 'Strasbourg',
    'mobility': 'Paris',
    'languages': 'Français, Anglais',
    'target_roles': 'AI Engineer, LLM Engineer, Data Scientist, Applied AI Engineer',
    'priority_locations': 'Strasbourg, Paris, Remote, France',
    'priority_keywords': 'python, sql, llm, rag, langchain, fastapi, pytorch, hugging face, qdrant, mlflow, langsmith, aws, gcp, data scientist, ai engineer',
    'cv_summary': 'Spécialisée en IA appliquée (LLM, RAG, architectures multi-agents), avec expérience en Python, SQL, FastAPI, LangChain, Qdrant, données de santé et modélisation prédictive.'
}


def load_profile():
    profile = {}
    for k, v in DEFAULT_PROFILE.items():
        profile[k] = get_setting(k) or v
    return profile


def save_profile(profile: dict):
    for k, v in profile.items():
        set_setting(k, v)
