class FBAExtractor:
    def __init__(self, tables):
        self.tables = tables

    def normalize_label(self, text):
        text = text.strip().lower()
        text = text.rstrip(":")
        text = " ".join(text.split())

        return text

    def find_value_after_labels(self, table, possible_labels, all_labels):
        normalized_possible_labels = {
            self.normalize_label(label)
            for label in possible_labels
        }

        normalized_all_labels = {
            self.normalize_label(label)
            for label in all_labels
        }

        for row_index, row in enumerate(table):
            for column_index, cell in enumerate(row):
                normalized_cell = self.normalize_label(cell)

                if normalized_cell in normalized_possible_labels:

                    # Case 1: value is in the next column
                    if column_index + 1 < len(row):
                        value = row[column_index + 1].strip()

                        if (
                            value
                            and self.normalize_label(value)
                            not in normalized_all_labels
                        ):
                            return value

                    # Case 2: value is in the same column on the next row
                    if row_index + 1 < len(table):
                        next_row = table[row_index + 1]

                        if column_index < len(next_row):
                            value = next_row[column_index].strip()

                            if (
                                value
                                and self.normalize_label(value)
                                not in normalized_all_labels
                            ):
                                return value

        return None

    def extract_identification(self):
        table = self.tables[0]

        field_labels = {
            "member_name": [
                "Member Name",
                "Client Name",
                "Patient Name",
            ],
            "member_dob": [
                "Member DOB",
                "Client DOB",
                "Patient DOB",
                "Date of Birth",
                "DOB",
            ],
            "cin": [
                "CIN #",
                "CIN",
                "Client Identification Number",
            ],
            "diagnosis": [
                "Diagnoses/with ICD Code",
                "Diagnosis",
                "Diagnosis with ICD Code",
                "ICD Diagnosis",
            ],
            "guardian_name": [
                "Guardian Name",
                "Parent/Guardian Name",
                "Caregiver Name",
            ],
            "phone": [
                "Phone",
                "Phone Number",
                "Contact Number",
            ],
            "primary_care_provider": [
                "Primary Care Provider",
                "PCP",
            ],
            "known_allergies": [
                "Known Allergies",
                "Allergies",
            ],
            "current_medications_dosage": [
                "Current Medications/Dosage",
                "Current Medications",
                "Medications",
            ],
            "dietary_restrictions": [
                "Dietary Restrictions",
                "Diet Restrictions",
            ],
            "lmhp_name_credential": [
                "Full name & Credential",
                "LMHP Name",
                "LMHP Name & Credential",
            ],
            "lmhp_contact_number": [
                "Contact Number",
                "LMHP Contact Number",
                "LMHP Phone",
            ],
        }

        # Flatten all aliases so the extractor can recognize when
        # the neighboring cell is another label instead of a value.
        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        identification = {}

        for field_name, aliases in field_labels.items():
            identification[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return identification