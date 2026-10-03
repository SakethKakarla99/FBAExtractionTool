from docx import Document


class DOCXExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.document = Document(file_path)

    def get_paragraphs(self):
        paragraphs = []

        for paragraph in self.document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return paragraphs
    def get_tables(self):
        tables = []

        for table in self.document.tables:
            table_data = []

            for row in table.rows:
                row_data = []

                for cell in row.cells:
                    text = cell.text.strip()

                    if not row_data or text != row_data[-1]:
                        row_data.append(text)

                table_data.append(row_data)

            tables.append(table_data)

        return tables