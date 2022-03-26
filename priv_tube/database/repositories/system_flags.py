from priv_tube.database.models.system_flags import SystemFlags as Model
from priv_tube.database import db


class SystemFlags:
    """
    Repository for interacting with the `system_flags` database table responsible for system-wide toggles.
    """

    @staticmethod
    def is_enabled(setting_name: str) -> bool:
        flag: Model = Model.query.filter_by(flag_name=setting_name).first()

        return bool(flag.value)

    @staticmethod
    def enable(setting_name: str):
        model: Model = Model.query.filter_by(flag_name=setting_name).first()
        model.value = True
        db.session.commit()

    @staticmethod
    def disable(setting_name: str):
        model: Model = Model.query.filter_by(flag_name=setting_name).first()
        model.value = False
        db.session.commit()
