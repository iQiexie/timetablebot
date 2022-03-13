def pydantic_converter(func):
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        if result is None:
            return result

        if hasattr(result, '__table__'):
            result_dict = dict((column.name, getattr(result, column.name)) for column in result.__table__.columns)
            final_result = args[0].schema(**result_dict)

            return final_result

    return wrapper
