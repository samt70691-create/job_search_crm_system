from src.db.init_db import init_db
from src.services.bootstrap_service import ensure_bootstrap
from src.services.automation_service import run_daily_maintenance
from src.services.export_service import export_jobs_to_excel
from src.services.report_service import build_summary_report

if __name__ == '__main__':
    init_db()
    ensure_bootstrap()
    run_daily_maintenance()
    export_jobs_to_excel()
    build_summary_report()
    print('Full setup complete.')
