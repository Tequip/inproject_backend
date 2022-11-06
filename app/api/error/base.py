from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self):
        pass


class HTTPExceptionAlreadyExists:
    status_code = 404

    @staticmethod
    def user():
        return HTTPException(status_code=HTTPExceptionAlreadyExists.status_code,
                             detail="Thw user with this email already exists")


class HTTPExceptionNotFound:
    status_code = 404

    @staticmethod
    def user():
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail="User not found")

    @staticmethod
    def project(project_id):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Project with id: {project_id} not found")

    @staticmethod
    def event(event_id):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Event with id: {event_id} not found")

    @staticmethod
    def resource(resource_id):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Resource with id: {resource_id} not found")

    @staticmethod
    def extension(extension_id):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Extension with id: {extension_id} not found")

    @staticmethod
    def extension_by_name(extension):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Extension {extension} not found")

    @staticmethod
    def stage(stage_id):
        return HTTPException(status_code=HTTPExceptionNotFound.status_code,
                             detail=f"Stage with id: {stage_id} not found")


class HTTPExceptionNotSupported:
    status_code = 415

    @staticmethod
    def extension(extension):
        return HTTPException(status_code=HTTPExceptionNotSupported.status_code,
                             detail=f"Extension {extension} not supported")


class HTTPExceptionPermission(HTTPException):
    status_code = 403

    @staticmethod
    def project(project_id):
        return HTTPException(status_code=HTTPExceptionPermission.status_code,
                             detail=f"You do not have permission to view project with id: {project_id}")


class HTTPExceptionAuth:

    @staticmethod
    def bad_token():
        return HTTPException(status_code=401,
                             detail="Could not validate credentials",
                             headers={"WWW-Authenticate": "Bearer"},)

    @staticmethod
    def expire_token():
        raise HTTPException(status_code=401,
                            detail="Access token expired",
                            headers={"WWW-Authenticate": "Bearer"},)

    @staticmethod
    def missing_token():
        pass

    @staticmethod
    def bad_credential():
        raise HTTPException(status_code=400, detail="Incorrect email or password")


class HTTPExceptionCloseRegistration(HTTPException):
    def __init__(self):
        super(HTTPExceptionCloseRegistration, self).__init__(status_code=403,
                                                             detail="User registration is not allowed on this server")
