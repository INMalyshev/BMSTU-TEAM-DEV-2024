from fastapi import FastAPI

from .cardset_router_builder import CardsetRouterBuilder
from ..sqlite_data import CardsetRepository, SqliteDbHandler
from ..core import CardsetService


class ApiAppBuilder:
    def __init__(self, *args, db_path: str = "test.db", **kwargs):
        super().__init__(*args, **kwargs)

        self.app = FastAPI(*args, **kwargs)

        self.db_handler = SqliteDbHandler(db_path)
        self.db_handler.initialize_db()
        self.cardset_repository = CardsetRepository(db_path)
        self.cardset_service = CardsetService(self.cardset_repository)
        self.router = CardsetRouterBuilder(self.cardset_service).router

        self.app.include_router(self.router)
