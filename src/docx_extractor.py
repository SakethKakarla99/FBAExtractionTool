from docx import Document
from docx.oxml.ns import qn


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
                    row_data.append(text)

                table_data.append(row_data)

            tables.append(table_data)

        return tables

    def get_yes_no_checkbox(self, table_index, row_index, cell_index):
        cell = self.document.tables[table_index].rows[row_index].cells[cell_index]

        checkbox_elements = cell._tc.xpath(
            './/*[local-name()="checkbox"]'
        )

        checkbox_states = []

        for checkbox in checkbox_elements:
            checked_elements = checkbox.xpath(
                './*[local-name()="checked"]'
            )

            if checked_elements:
                checked_element = checked_elements[0]

                value = None

                for attribute_name, attribute_value in checked_element.attrib.items():
                    if attribute_name.endswith("}val") or attribute_name == "val":
                        value = attribute_value
                        break

                checkbox_states.append(value == "1")

        if len(checkbox_states) < 2:
            return None

        yes_checked = checkbox_states[0]
        no_checked = checkbox_states[1]

        if yes_checked and not no_checked:
            return "Yes"

        if no_checked and not yes_checked:
            return "No"

        return None

    def get_yes_no_checkbox_by_label(self, possible_labels):
        normalized_labels = [
            " ".join(label.strip().lower().rstrip(":").split())
            for label in possible_labels
        ]

        for table in self.document.tables:
            for row in table.rows:

                for cell_index, cell in enumerate(row.cells):
                    normalized_cell = " ".join(
                        cell.text.strip().lower().rstrip(":").split()
                    )

                    label_found = any(
                        normalized_cell == label
                        or normalized_cell.startswith(label + ":")
                        for label in normalized_labels
                    )

                    if not label_found:
                        continue

                    # Search the other cells in this row for Yes/No checkboxes
                    for value_cell in row.cells:
                        checkbox_elements = value_cell._tc.xpath(
                            './/*[local-name()="checkbox"]'
                        )

                        if len(checkbox_elements) < 2:
                            continue

                        checkbox_states = []

                        for checkbox in checkbox_elements:
                            checked_elements = checkbox.xpath(
                                './*[local-name()="checked"]'
                            )

                            if not checked_elements:
                                continue

                            checked_element = checked_elements[0]

                            value = None

                            for attribute_name, attribute_value in checked_element.attrib.items():
                                if (
                                    attribute_name.endswith("}val")
                                    or attribute_name == "val"
                                ):
                                    value = attribute_value
                                    break

                            checkbox_states.append(value == "1")

                        if len(checkbox_states) < 2:
                            continue

                        yes_checked = checkbox_states[0]
                        no_checked = checkbox_states[1]

                        if yes_checked and not no_checked:
                            return "Yes"

                        if no_checked and not yes_checked:
                            return "No"

                        return None

        return None