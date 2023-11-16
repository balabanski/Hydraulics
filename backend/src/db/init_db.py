from backend.src.db.session import engine


# -----------------------------create_db_and_tables---------------------------------------------
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ---------------------------------create_data----------------------------------------------
async def create_init_data() -> None:
    # async with SessionLocal() as session:
    with Session(engine) as session:
        user_1 = User(
            name="Vanya",
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
        file_4.user = user_1
        # await session.commit()
        session.commit()


async def main() -> None:
    logger.info("Creating initial data")
    # create_db_and_tables()
    # await create_init_data()
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
