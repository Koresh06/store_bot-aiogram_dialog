from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.user import UserRepo
from app.database.repo.admin import AdminRepo


@dataclass
class RequestsRepo:

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        
        return UserRepo(self.session)


    @property
    def admin(self) -> AdminRepo:
        
        return AdminRepo(self.session)
   