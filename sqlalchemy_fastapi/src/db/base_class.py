from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

# This transform the bellow class into a base class Model
@as_declarative()
class Base:
    id: Any
    __name__: str
    
    # Generate table name automatically using lower class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"