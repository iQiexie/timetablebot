# Import all the models, so that Base has them before being
# imported by Alembic
from app.backend.db.base_model import Base  # noqa
from app.backend.db.models.action import UserActionModel  # noqa
from app.backend.db.models.classes import ClassModel  # noqa
from app.backend.db.models.credentials import CredentialsModel  # noqa
from app.backend.db.models.user import ExternalUserModel  # noqa
from app.backend.db.models.user import UserModel  # noqa
