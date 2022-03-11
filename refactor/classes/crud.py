from typing import List

from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from refactor.base.crud import BaseCRUD
from refactor.base.utils import columns_to_pydantic
from refactor.classes.models import Class, Hyperlink
from refactor.classes.schemas import ClassSchema, HyperlinkSchema


class ClassesCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = Class
        self.schema = ClassSchema

        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)
        self.hyperlinks = BaseCRUD(db_session=db_session, model=Hyperlink, schema=HyperlinkSchema)

    async def create(self, **kwargs):
        async with self.base.transaction():
            hyperlink_list = kwargs.get("hyperlinks")
            kwargs.pop("hyperlinks")
            returning_model = await self.base.insert(**kwargs)

            for hyperlink in hyperlink_list:
                if hyperlink is not None:
                    await self.hyperlinks.insert(
                        class_id=returning_model.id,
                        hyperlink=hyperlink
                    )

            return returning_model

    async def get(self, group_id: int, week_day_index: int, above_line: bool) -> List[ClassSchema]:
        async with self.base.transaction():
            result = await self.base.get_many(and_(
                self.model.group_id == group_id,
                self.model.week_day_index == week_day_index,
                self.model.above_line == above_line
            ))

        result_list = []

        for sub_result in result:
            class_model = columns_to_pydantic(sub_result, ClassSchema)
            class_model.hyperlinks = []

            async with self.hyperlinks.transaction():
                hyperlinks = await self.hyperlinks.get_many(self.hyperlinks.model.class_id == sub_result.id)

            for hyperlink in hyperlinks:
                print(hyperlink)
                hyperlink_model = columns_to_pydantic(hyperlink, HyperlinkSchema)
                class_model.hyperlinks.append(hyperlink_model.hyperlink)

            result_list.append(class_model)

        return result_list

    async def update(self, group_id: int, absolute_index: int, **kwargs):
        async with self.base.transaction():
            return await self.base.update(
                and_(self.model.group_id == group_id, self.model.absolute_index == absolute_index),
                **kwargs
            )

    async def delete(self, group_id: int, absolute_index: int):
        async with self.base.transaction():
            return await self.base.delete((and_(
                self.model.group_id == group_id,
                self.model.absolute_index == absolute_index
            )))

    async def empty_table(self):
        async with self.base.transaction():
            await self.hyperlinks.delete(self.hyperlinks.model.id == self.hyperlinks.model.id)
            await self.base.delete(self.model.id == self.model.id)
