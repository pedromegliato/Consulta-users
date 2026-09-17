from typing import Annotated

from fastapi import Depends, Request

from app.application.fetch_users import FetchUsersService
from app.application.list_users import ListUsersService
from app.core.container import Services


def get_services(request: Request) -> Services:
    services: Services = request.app.state.services
    return services


ServicesDep = Annotated[Services, Depends(get_services)]


def get_fetch_users_service(services: ServicesDep) -> FetchUsersService:
    return services.fetch_users


def get_list_users_service(services: ServicesDep) -> ListUsersService:
    return services.list_users


FetchUsersServiceDep = Annotated[FetchUsersService, Depends(get_fetch_users_service)]
ListUsersServiceDep = Annotated[ListUsersService, Depends(get_list_users_service)]
