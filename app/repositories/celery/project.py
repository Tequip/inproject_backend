from sqlalchemy import delete, select, distinct, not_
from app.models.entity.project import project_table, a_project_relation_table, a_project_member_order_table, \
    a_project_category_table, a_project_member_recommend_table, a_project_category_predict_table
from app.models.entity.category import category_table


class ProjectRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def get_many(self, project_ids):
        query = select([project_table]).where(project_table.c.id.in_(project_ids))
        records = self.connection.execute(query)
        return records.fetchall()

    def all(self):
        query = select(project_table.c.id).where(not_(project_table.c.is_hidden))
        records = self._connection.execute(query)
        return self.get_many([record["id"] for record in records])

    def create_relation_project(self, project_id, relation_project_id, score):
        query = a_project_relation_table.insert().values(project_id=project_id,
                                                         relation_project_id=relation_project_id,
                                                         score=score)
        self.connection.execute(query)

    def delete_relation_project(self):
        # TODO временное решение переписать на upsert
        query = delete(a_project_relation_table)
        self.connection.execute(query)

    def get_member_order(self):
        query = select([distinct(project_table.c.id),
                        a_project_member_order_table.c.role,
                        category_table.c.name]).select_from(
            project_table.join(a_project_member_order_table).join(a_project_category_table).join(category_table)
        ).where(not_(project_table.c.is_hidden))
        records = self.connection.execute(query)
        return records.fetchall()

    def create_project_user_recommend(self, project_id, user_id, fits):
        query = a_project_member_recommend_table.insert().values(project_id=project_id,
                                                                 user_id=user_id,
                                                                 fits=fits)
        self.connection.execute(query)

    def delete_recommendation_users_and_projects(self):
        # TODO временное решение переписать на upsert
        query = delete(a_project_member_recommend_table)
        self.connection.execute(query)

    def create_project_predict_category(self, project_id, category_id, similarity):
        query = a_project_category_predict_table.insert().values(project_id=project_id,
                                                                 category_id=category_id,
                                                                 similarity=similarity)

        self.connection.execute(query)

    def delete_project_predict_category(self):
        # TODO временное решение переписать на upsert
        query = delete(a_project_category_predict_table)
        self.connection.execute(query)
