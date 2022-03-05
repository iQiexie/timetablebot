from refactor.classes.crud import ClassesCRUD
from refactor.google_api.schemas import ColumnSchema


async def create_classes(spreadsheet_column: ColumnSchema, db: ClassesCRUD):
    pass


async def test(db: ClassesCRUD):
    print('test')