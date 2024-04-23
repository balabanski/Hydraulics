import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from backend.src.core.config import settings
# from backend.src.db.session import engine
from backend.src.models import Directory, File, User


logger: logging.Logger = logging.getLogger(__name__)
engine = create_async_engine(settings.sqlite_url, echo=settings.DEBUG)
print(engine.url)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# -----------------------------create_db_and_tables---------------------------------------------
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    # SQLModel.metadata.create_all(engine)


# ---------------------------------create_data----------------------------------------------
async def create_init_data() -> None:
    async with SessionLocal() as session:
        # with Session(engine) as session:
        user_1 = User(
            full_name="Vanya",
            email="vania50505050@gmail.com",
            hashed_password="97014b6d26954784abddecae3b7b67f6",
        )
        file_1 = File(name="Prestel_main")

        directory_1 = Directory(name="Prestel")
        dir_2 = Directory(name="kantovatel")
        file_2 = File(name="main(of dir Prestel)")
        file_3 = File(name="kantovatel_main")
        file_4 = File(name="cyl_for Sacha")

        session.add(user_1)
        user_1.files = [file_1]
        user_1.directories = [directory_1, dir_2]
        directory_1.files = [file_2]
        dir_2.files = [file_3]

        session.add(file_4)
        file_4.user = user_1

        await session.commit()
        # session.commit()


async def main() -> None:
    logger.info("Creating initial data")
    await create_db_and_tables()

    await create_init_data()
    # await select_dir_and_file()
    # await get_metadata_from_db(name_file= "Prestel_main")
    # update_file(6,FileUpdate(meta_data={'value': 'Petiusha'}))
    # create_file_in_directory(File(name='cyl_for Sacha', directory_id=2, meta_data={'p1':250}))
    # create_user("Petya")
    # create_file('file_userPetya', 2)
    # delete_file(9)

    # logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
