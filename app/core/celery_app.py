import pickle
import pandas as pd
from celery import Celery
from sqlalchemy import create_engine

from app.repositories.celery.project import ProjectRepository
from app.repositories.celery.audit import AuditRepository
from app.repositories.celery.user import UserRepository
from app.repositories.celery.category import CategoryRepository
from ml.main import get_related, calculate_recommendation_users_and_projects, get_top_tags
from app.services.security import security_service
from app.core.config import settings


engine = create_engine(settings.PG_CELERY_DSN, pool_pre_ping=True, pool_size=30)
celery_app = Celery('tasks', broker=settings.BROKER_URL)

celery_app.conf.update(
    task_serializer='pickle',
    accept_content=['pickle'],  # Ignore other content
    result_serializer='pickle')


@celery_app.task
def recommendation_users_and_projects():
    with engine.begin() as db:
        project_repo = ProjectRepository(db)
        projects = project_repo.get_member_order()

        user_repo = UserRepository(db)
        users = user_repo.all()
        if projects is not None and users is not None:
            d_project = {"id": [project["id"]for project in projects],
                         "open_vacancy": [project["role"]for project in projects],
                         "category": [project["name"]for project in projects]}
            df_project = pd.DataFrame(data=d_project)

            d_user = {"id": [], "position": [], "interest": []}
            for user in users:
                if user["role"] is None:
                    continue
                user_interest = user_repo.get_interest(user["id"])
                if not len(user_interest):
                    continue
                d_user["id"].append(user["id"])
                d_user["position"].append(user["role"])
                d_user["interest"].append(user_interest)

            df_user = pd.DataFrame(data=d_user)

            if len(df_user) and len(df_project):
                # TODO временное решение переписать на upsert
                project_repo.delete_recommendation_users_and_projects()
                df_1, df_2 = calculate_recommendation_users_and_projects(df_project, df_user)
                for index, row in df_1.iterrows():
                    project_repo.create_project_user_recommend(row['id_project'], row['id_user'], row['cosine'])
                for index, row in df_2.iterrows():
                    project_repo.create_project_user_recommend(row['id_project'], row['id_user'], row['cosine'])


@celery_app.task
def project_predict_category():
    with engine.begin() as db:
        project_repo = ProjectRepository(db)
        projects = project_repo.all()

        category_repo = CategoryRepository(db)
        categories = category_repo.all()

        d_project = {"id": [project["id"] for project in projects],
                     "text": [project["about"] for project in projects]}
        df_project = pd.DataFrame(data=d_project)

        d_category = {"id": [category["id"] for category in categories],
                      "name": [category["name"] for category in categories]}
        df_category = pd.DataFrame(data=d_category)

        if len(d_category) and len(df_project):
            # TODO временное решение переписать на upsert
            project_repo.delete_project_predict_category()
            df = get_top_tags(df_project, df_category)
            for index, row in df.iterrows():
                project_repo.create_project_predict_category(row["project_id"], row["tag"], row["score"])


@celery_app.task
def relation_project():
    with engine.begin() as db:
        project_repo = ProjectRepository(db)
        # TODO временное решение переписать на upsert
        project_repo.delete_relation_project()
        projects = project_repo.all()
        projects_ids = [project["id"] for project in projects]
        project_title = [project["about"] for project in projects]
        df = get_related(projects_ids, project_title)
        for index, row in df.iterrows():
            project_repo.create_relation_project(row['original_project'], row['related_project'], row['score'])


@celery_app.task
def audit(data):
    data_dict = pickle.loads(data)
    with engine.begin() as db:
        audit_repo = AuditRepository(db)
        agent = ""
        user_id = None
        for name, value in data_dict["headers"].items():
            if name == "user-agent":
                agent = value

            if name == "authorization":
                args = value.split(' ')
                if args[0] == "Bearer":
                    try:
                        token_data = security_service.verify_token(args[1])
                        user_id = token_data.user_id
                    except Exception:
                        pass

        if user_id is not None:
            audit_repo.insert(data_dict["datetime"], user_id, data_dict["method"], str(data_dict["url"]), agent, "{}")
