from pathlib import Path

from alembic.config import Config

from alembic import command


def upgrade(engine):
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "alembic"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
