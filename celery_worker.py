from app import create_app,celery
app = create_app()
app.app_context().push()
#celery -A celery_worker.celery worker -l info