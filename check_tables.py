from sqlalchemy import inspect, create_engine

# نفس الرابط اللي عندك في database.py لكن بصيغة sync
DATABASE_URL = "sqlite:///./ai_agent.db"

# Create sync engine
engine = create_engine(DATABASE_URL, echo=False)

# Inspect the database
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:", tables)