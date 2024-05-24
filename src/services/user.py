from ..schemas import UserSchema, UserRegistrationSchema
from ..exceptions import UserByUsernameNotFoundException, UserByIdNotFoundException, UserConflictException
from ..exceptions import ConflictException
from ..utils.security import get_hashed_password
from ..utils.unit_of_work import IUnitOfWork


class UserService:
    @staticmethod
    async def get_user_by_id(uow: IUnitOfWork, user_id: str) -> UserSchema:
        async with uow:
            user = await uow.users.get_one(id=user_id)
            if not user:
                raise UserByIdNotFoundException(user_id)
            return user

    @staticmethod
    async def get_user_by_username(uow: IUnitOfWork, username: str) -> UserSchema:
        async with uow:
            user = await uow.users.get_one(username=username)
            if not user:
                raise UserByUsernameNotFoundException(username)
            return user

    @staticmethod
    async def create_user(uow: IUnitOfWork, user: UserRegistrationSchema) -> UserSchema:
        async with uow:
            try:
                is_exists = await uow.users.is_exists(username=user.username)
                if is_exists:
                    raise UserConflictException(f"User with username '{user.username}' already exists")
                is_exists = await uow.users.is_exists(username=user.email)
                if is_exists:
                    raise UserConflictException(f"User with email '{user.email}' already exists")
                user.password = get_hashed_password(user.password)
                user: UserSchema = await uow.users.create_one(data=user.model_dump())
                await uow.commit()
                return user
            except ConflictException:
                raise UserConflictException()
