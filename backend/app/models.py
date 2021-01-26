from sqlalchemy import Column, DateTime, Integer, MetaData, String, func, Table

metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("author", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
    Column("updated_date", DateTime, default=func.now(), onupdate=func.now()),
)