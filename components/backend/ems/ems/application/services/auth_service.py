from enum import auto, IntEnum
from typing import Optional

from attr import dataclass

from ems.application import dto, entities
from ems.application.interfaces import (
    IUserRepository,
    IInstitutionRepository,
)
from ems_libs.security import Hasher

import re


class LoginResult(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    WRONG_PASSWORD = auto()


class RegistrationStatus(IntEnum):
    OK = auto()
    EMAIL_TAKEN = auto()
    BAD_REQUEST = auto()
    UNEXPECTED_ERROR = auto()
    INSTITUTION_NOT_FOUND = auto()


@dataclass
class AuthService:
    user_repository: IUserRepository
    institution_repository: IInstitutionRepository

    async def login(
            self,
            body: dto.LoginRequest
    ) -> tuple[Optional[entities.User], LoginResult]:
        db_user = await self.user_repository.get_by_email(body.email)
        if db_user is None:
            return None, LoginResult.NOT_FOUND
        if not Hasher.verify_hash(body.password, db_user.password):
            return None, LoginResult.WRONG_PASSWORD
        return db_user, LoginResult.OK

    async def register_student(
            self,
            body: dto.UserCreateRequest
    ) -> tuple[Optional[entities.User], RegistrationStatus]:
        if await self.user_repository.is_email_taken(body.email):
            return None, RegistrationStatus.EMAIL_TAKEN

        if not AuthService.check_password(body.password)\
           or not AuthService.check_email(body.email)\
           or body.telegram is not None and not AuthService.check_telegram(body.telegram)\
           or body.vk is not None and not AuthService.check_vk(body.vk)\
           or body.phone_number is not None and not AuthService.check_phone(body.phone_number):
            return None, RegistrationStatus.BAD_REQUEST

        institution = await self.institution_repository.get_by_id(body.institution_id)
        if institution is None:
            return None, RegistrationStatus.INSTITUTION_NOT_FOUND

        user_id = await self.user_repository.add_one(body)
        if user_id is None:
            return None, RegistrationStatus.UNEXPECTED_ERROR

        db_user = await self.user_repository.get_by_id(user_id)
        return db_user, RegistrationStatus.OK

    @staticmethod
    def check_password(password: str) -> bool:
        return re.match(r'^\S+$', password) is not None

    @staticmethod
    def check_email(email: str) -> bool:
        expr = r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$'
        return re.match(expr, email) is not None

    @staticmethod
    def check_telegram(telegram: str) -> bool:
        return re.match(r'^[a-z0-9_]{5,32}$', telegram) is not None

    @staticmethod
    def check_vk(vk: str) -> bool:
        return re.match(r'^[a-z0-9_]{5,32}$', vk) is not None

    @staticmethod
    def check_phone(phone: str) -> bool:
        expr = r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$'
        return re.match(expr, phone) is not None
