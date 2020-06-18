from dependency_injector import providers, containers

from backend.services.location_data_service import LocationDataService
from backend.core.libs.cache import Cache
from backend.services.data_source_service import DataSources

class Container(containers.DeclarativeContainer): # TODO: Split into multiple containers?
    cache = providers.Singleton(Cache)

class DataSourceContainer(containers.DeclarativeContainer):
    data_sources = providers.Singleton(DataSources)
    location_data_service = providers.Singleton(LocationDataService)