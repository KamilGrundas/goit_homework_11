from sqlalchemy import create_engine

# uri = "sqlite:///superblog"
uri = "postgresql://worker:secret@localhost:5432/superblog"
engine = create_engine(uri)
