class FBAExtractor:
    def __init__(self, tables):
        self.tables = tables

    def find_value_after_label(self, table, label):
        for row_index, row in enumerate(table):
            for column_index, cell in enumerate(row):

                if cell.strip() == label:
                    next_row_index = row_index + 1

                    if next_row_index < len(table):
                        next_row = table[next_row_index]

                        if column_index < len(next_row):
                            return next_row[column_index]

        return None

    def extract_identification(self):
        table = self.tables[0]

        identification = {
            "member_name": self.find_value_after_label(table, "Member Name:"),
            "member_dob": self.find_value_after_label(table, "Member DOB:"),
            "cin": self.find_value_after_label(table, "CIN #"),
            "diagnosis": self.find_value_after_label(table, "Diagnoses/with ICD Code:"),
            "guardian_name": self.find_value_after_label(table, "Guardian Name:"),
            "phone": self.find_value_after_label(table, "Phone:"),
            "primary_care_provider": self.find_value_after_label(
                table, "Primary Care Provider:"
            ),
            "known_allergies": self.find_value_after_label(
                table, "Known Allergies:"
            ),
            "current_medications_dosage": self.find_value_after_label(
                table, "Current Medications/Dosage:"
            ),
            "dietary_restrictions": self.find_value_after_label(
                table, "Dietary Restrictions:"
            ),
            "lmhp_name_credential": self.find_value_after_label(
                table, "Full name & Credential"
            ),
            "lmhp_contact_number": self.find_value_after_label(
                table, "Contact Number"
            ),
        }

        return identification