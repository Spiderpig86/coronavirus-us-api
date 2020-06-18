from dependency_injector import containers, providers

from backend.core.libs.cache import Cache
from backend.services.data_source_service import DataSources
from backend.services.location_data_service import LocationDataService


class Container(
    containers.DeclarativeContainer
):  # TODO: Split into multiple containers?
    cache = providers.Singleton(Cache)


class DataSourceContainer(containers.DeclarativeContainer):
    data_sources = providers.Singleton(DataSources)
    location_data_service = providers.Singleton(LocationDataService)
