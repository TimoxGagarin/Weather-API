from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, session, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(
        cls, session, offset: int | None = None, limit: int | None = None, **filter_by
    ):
        query = (
            select(cls.model)
            .filter_by(**filter_by)
            .options(selectinload("*"))
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session, **data):
        instance = cls.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def add_all(cls, session, rows: list[dict]):
        instances = [cls.model(**row) for row in rows]
        session.add_all(instances)
        await session.commit()
        for instance in instances:
            await session.refresh(instance)
        return instances

    @classmethod
    async def update(cls, session, id, **data):
        data = {key: value for key, value in data.items() if value is not None}

        query = (
            update(cls.model)
            .filter_by(id=id)
            .values(**data)
            .returning(cls.model)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        await session.commit()

        updated_instance = result.unique().scalar_one_or_none()
        if updated_instance:
            await session.refresh(updated_instance)
        return updated_instance

    @classmethod
    async def delete(cls, session, **data):
        query = delete(cls.model).filter_by(**data)
        await session.execute(query)
        await session.commit()
