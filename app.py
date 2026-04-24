import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from src.db.init_db import init_db

st.set_page_config(
    page_title="Job Search CRM",
    page_icon="📌",
    layout="wide",
)

init_db()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "app.db"


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def table_exists(conn, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def safe_read_sql(conn, query: str, params=None):
    try:
        return pd.read_sql_query(query, conn, params=params or ())
    except Exception:
        return pd.DataFrame()


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df.columns = [str(c) for c in df.columns]
    return df


def ensure_candidate_profile_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS candidate_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            headline TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            mobility TEXT,
            target_roles TEXT,
            priority_locations TEXT,
            priority_keywords TEXT,
            cv_summary TEXT,
            languages TEXT
        )
        """
    )
    conn.commit()


def get_profile(conn):
    ensure_candidate_profile_table(conn)

    df = safe_read_sql(conn, "SELECT * FROM candidate_profile LIMIT 1")
    if df.empty:
        return {
            "candidate_name": "",
            "headline": "",
            "email": "",
            "phone": "",
            "location": "",
            "mobility": "",
            "target_roles": "",
            "priority_locations": "",
            "priority_keywords": "",
            "cv_summary": "",
            "languages": "",
        }

    row = df.iloc[0].to_dict()
    return {
        "candidate_name": row.get("candidate_name", ""),
        "headline": row.get("headline", ""),
        "email": row.get("email", ""),
        "phone": row.get("phone", ""),
        "location": row.get("location", ""),
        "mobility": row.get("mobility", ""),
        "target_roles": row.get("target_roles", ""),
        "priority_locations": row.get("priority_locations", ""),
        "priority_keywords": row.get("priority_keywords", ""),
        "cv_summary": row.get("cv_summary", ""),
        "languages": row.get("languages", ""),
    }


def save_profile(conn, profile: dict):
    ensure_candidate_profile_table(conn)

    existing = conn.execute("SELECT id FROM candidate_profile LIMIT 1").fetchone()

    if existing:
        conn.execute(
            """
            UPDATE candidate_profile
            SET candidate_name=?,
                headline=?,
                email=?,
                phone=?,
                location=?,
                mobility=?,
                target_roles=?,
                priority_locations=?,
                priority_keywords=?,
                cv_summary=?,
                languages=?
            WHERE id=?
            """,
            (
                profile["candidate_name"],
                profile["headline"],
                profile["email"],
                profile["phone"],
                profile["location"],
                profile["mobility"],
                profile["target_roles"],
                profile["priority_locations"],
                profile["priority_keywords"],
                profile["cv_summary"],
                profile["languages"],
                existing[0],
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO candidate_profile (
                candidate_name,
                headline,
                email,
                phone,
                location,
                mobility,
                target_roles,
                priority_locations,
                priority_keywords,
                cv_summary,
                languages
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile["candidate_name"],
                profile["headline"],
                profile["email"],
                profile["phone"],
                profile["location"],
                profile["mobility"],
                profile["target_roles"],
                profile["priority_locations"],
                profile["priority_keywords"],
                profile["cv_summary"],
                profile["languages"],
            ),
        )

    conn.commit()


def show_dataframe(df: pd.DataFrame, preferred_columns=None):
    df = normalize_columns(df)
    if df.empty:
        st.info("Aucune donnée à afficher.")
        return

    if preferred_columns:
        visible_cols = [c for c in preferred_columns if c in df.columns]
        if visible_cols:
            df = df[visible_cols]

    st.dataframe(df, width="stretch", hide_index=True)


conn = get_conn()

offers_df = (
    safe_read_sql(conn, "SELECT * FROM job_offers ORDER BY COALESCE(score, 0) DESC, id DESC")
    if table_exists(conn, "job_offers")
    else pd.DataFrame()
)

applications_df = (
    safe_read_sql(conn, "SELECT * FROM applications ORDER BY id DESC")
    if table_exists(conn, "applications")
    else pd.DataFrame()
)

contacts_df = (
    safe_read_sql(conn, "SELECT * FROM contacts ORDER BY id DESC")
    if table_exists(conn, "contacts")
    else pd.DataFrame()
)

masters_df = (
    safe_read_sql(conn, "SELECT * FROM masters_programs ORDER BY COALESCE(score, 0) DESC, id DESC")
    if table_exists(conn, "masters_programs")
    else pd.DataFrame()
)

offers_df = normalize_columns(offers_df)
applications_df = normalize_columns(applications_df)
contacts_df = normalize_columns(contacts_df)
masters_df = normalize_columns(masters_df)

offers_count = len(offers_df)
new_count = (
    len(offers_df[offers_df["status"].astype(str).str.lower().eq("new")])
    if "status" in offers_df.columns
    else 0
)
to_apply_count = (
    len(offers_df[offers_df["status"].astype(str).str.lower().isin(["to_apply", "a_postuler", "à postuler"])])
    if "status" in offers_df.columns
    else 0
)
applications_count = len(applications_df)
followup_count = (
    len(applications_df[applications_df["application_status"].astype(str).str.lower().eq("followup_due")])
    if "application_status" in applications_df.columns
    else 0
)
contacts_count = len(contacts_df)

st.title("Job Search CRM")
st.caption("Pilotage des offres, candidatures, contacts et masters")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Offres", offers_count)
c2.metric("Nouvelles", new_count)
c3.metric("À postuler", to_apply_count)
c4.metric("Candidatures", applications_count)
c5.metric("Relances", followup_count)
c6.metric("Contacts", contacts_count)

st.info("Système prêt. Utilise le menu ci-dessous.")

page = st.selectbox(
    "Choisis une section",
    ["Accueil", "Offres", "Candidatures", "Contacts", "Masters", "Paramètres"],
)

if page == "Accueil":
    st.subheader("Vue d'ensemble")

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("### Top offres")
        show_dataframe(
            offers_df.head(10),
            preferred_columns=[
                "id",
                "title",
                "company",
                "location",
                "score",
                "status",
                "source",
            ],
        )

    with right:
        st.markdown("### Relances à faire")
        if not applications_df.empty and "application_status" in applications_df.columns:
            due_df = applications_df[
                applications_df["application_status"].astype(str).str.lower().eq("followup_due")
            ]
        else:
            due_df = pd.DataFrame()

        show_dataframe(
            due_df.head(10),
            preferred_columns=[
                "id",
                "job_offer_id",
                "application_status",
                "next_followup_date",
                "notes",
            ],
        )

elif page == "Offres":
    st.subheader("Offres")

    filtered = offers_df.copy()

    col1, col2, col3 = st.columns(3)

    keyword = col1.text_input("Mot-clé")
    status_options = (
        ["Tous"] + sorted(filtered["status"].dropna().astype(str).unique().tolist())
        if "status" in filtered.columns
        else ["Tous"]
    )
    status_filter = col2.selectbox("Statut", status_options)
    company_filter = col3.text_input("Entreprise")

    if keyword:
        mask = pd.Series(False, index=filtered.index)
        for col in ["title", "company", "location", "description"]:
            if col in filtered.columns:
                mask = mask | filtered[col].astype(str).str.contains(keyword, case=False, na=False)
        filtered = filtered[mask]

    if status_filter != "Tous" and "status" in filtered.columns:
        filtered = filtered[filtered["status"].astype(str) == status_filter]

    if company_filter and "company" in filtered.columns:
        filtered = filtered[filtered["company"].astype(str).str.contains(company_filter, case=False, na=False)]

    st.write(f"{len(filtered)} offre(s) affichée(s).")

    show_dataframe(
        filtered,
        preferred_columns=[
            "id",
            "title",
            "company",
            "location",
            "contract_type",
            "score",
            "status",
            "source",
            "url",
            "created_at",
        ],
    )

elif page == "Candidatures":
    st.subheader("Candidatures")
    show_dataframe(
        applications_df,
        preferred_columns=[
            "id",
            "job_offer_id",
            "application_status",
            "application_date",
            "next_followup_date",
            "notes",
            "created_at",
        ],
    )

elif page == "Contacts":
    st.subheader("Contacts")
    show_dataframe(
        contacts_df,
        preferred_columns=[
            "id",
            "full_name",
            "company",
            "job_title",
            "email",
            "phone",
            "linkedin_url",
            "contact_type",
            "notes",
        ],
    )

elif page == "Masters":
    st.subheader("Masters & Formations")
    show_dataframe(
        masters_df,
        preferred_columns=[
            "id",
            "program_name",
            "institution",
            "city",
            "score",
            "status",
            "url",
            "deadline",
        ],
    )

elif page == "Paramètres":
    st.subheader("Paramètres & Profil")

    profile = get_profile(conn)

    with st.form("profile_form"):
        candidate_name = st.text_input("Nom", value=profile["candidate_name"])
        headline = st.text_input("Titre", value=profile["headline"])
        email = st.text_input("Email", value=profile["email"])
        phone = st.text_input("Téléphone", value=profile["phone"])
        location = st.text_input("Localisation", value=profile["location"])
        mobility = st.text_input("Mobilité", value=profile["mobility"])
        target_roles = st.text_area("Postes cibles", value=profile["target_roles"], height=120)
        priority_locations = st.text_area("Lieux prioritaires", value=profile["priority_locations"], height=100)
        priority_keywords = st.text_area("Mots-clés prioritaires", value=profile["priority_keywords"], height=120)
        cv_summary = st.text_area("Résumé CV", value=profile["cv_summary"], height=180)
        languages = st.text_input("Langues", value=profile["languages"])

        submitted = st.form_submit_button("Sauvegarder le profil")

        if submitted:
            save_profile(
                conn,
                {
                    "candidate_name": candidate_name,
                    "headline": headline,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "mobility": mobility,
                    "target_roles": target_roles,
                    "priority_locations": priority_locations,
                    "priority_keywords": priority_keywords,
                    "cv_summary": cv_summary,
                    "languages": languages,
                },
            )
            st.success("Profil sauvegardé avec succès.")

    st.markdown("### Aperçu du profil")
    refreshed_profile = get_profile(conn)
    st.json(refreshed_profile)

conn.close()
