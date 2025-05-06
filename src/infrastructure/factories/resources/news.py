# coding utf-8

from fastapi import Depends

from ....domain.core.settings import AppSettings
from ...settings.core import get_app_settings

from ...orm.db.core import Database
from ...orm.db.repositories import NewsRepositry

from ....services.resources import NewsService
from ...api.views.v1 import NewsView


class NewsRepositoryFactory:
    @staticmethod
    def get(
        settings: AppSettings = Depends(get_app_settings),
    ) -> NewsRepositry:
        return NewsRepositry(Database(settings))


class NewsServiceFactory:
    @staticmethod
    def get(
        repository: NewsRepositry = Depends(
            NewsRepositoryFactory.get,
        ),
    ) -> NewsService:
        return NewsService(repository)


class NewsViewFactory:
    @staticmethod
    def create(
        service: NewsService = Depends(
            NewsServiceFactory.get,
        ),
    ) -> NewsView:
        return NewsView(service)
