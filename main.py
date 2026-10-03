from src.docx_extractor import DOCXExtractor
from src.fba_extractor import FBAExtractor


FILE_PATH = "documents/fba.docx"

docx_extractor = DOCXExtractor(FILE_PATH)

tables = docx_extractor.get_tables()

fba_extractor = FBAExtractor(tables)

identification = fba_extractor.extract_identification()

print("\n========== IDENTIFICATION ==========")

for key, value in identification.items():
    print(f"{key}: {value}")