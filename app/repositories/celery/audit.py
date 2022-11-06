from app.models.audit.audit import audit_table


class AuditRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def insert(self, ts, user_id, method, url, agent, params):
        # TODO переписать на pydantic схему
        query = audit_table.insert().values(ts=ts, user_id=user_id, method=method, url=url,
                                            agent=agent, params=params)
        self.connection.execute(query)
