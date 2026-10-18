"""Local maintenance; never accepts passwords in command arguments."""
import argparse
import getpass
import os
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import default_database_url, make_engine
from app.models import User
from app.migrations import upgrade
from app.security import bootstrap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["migrate", "create-admin"])
    parser.add_argument("--username", default="admin")
    args = parser.parse_args()
    engine = make_engine(os.getenv("SII_MB_DATABASE_URL") or default_database_url())
    upgrade(engine)
    if args.command == "create-admin":
        with Session(engine) as session:
            if session.scalar(select(User.id).limit(1)):
                raise SystemExit("Ya hay usuarios; administra las cuentas desde la aplicación")
            bootstrap(session, args.username, getpass.getpass("Contraseña inicial (mínimo 12 caracteres): "))
            print("Cuenta administrativa creada")
    else:
        print("Base actualizada")
    engine.dispose()


if __name__ == "__main__":
    main()
