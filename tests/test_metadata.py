from app.metadata.loader import load_all_metadata

metadata = load_all_metadata()

print(metadata["fiscal_calendar"])

