class FBAExtractor:
    def __init__(self, tables, docx_extractor = None):
        self.tables = tables
        self.docx_extractor = docx_extractor

    def normalize_label(self, text):
        text = text.strip().lower()
        text = text.rstrip(":")
        text = " ".join(text.split())

        return text

    def find_table(self, possible_labels):
        normalized_labels = {
            self.normalize_label(label)
            for label in possible_labels
        }

        for table in self.tables:
            for row in table:
                for cell in row:
                    normalized_cell = self.normalize_label(cell)

                    for label in normalized_labels:
                        if (
                            normalized_cell == label
                            or normalized_cell.startswith(label + ":")
                            or normalized_cell.startswith(label + " ")
                        ):
                            return table

        return None

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

                matched_label = any(
                    normalized_cell == label
                    or normalized_cell.startswith(label + ":")
                    for label in normalized_possible_labels
                )

                if matched_label:

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
        table = self.find_table([
        "Member Name",
        "Client Name",
        "Patient Name",])

        if table is None:
            return {}

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

    def extract_service_history(self):
        table = self.find_table([
            "Service Initiation Date",
            "Service Start Date",
            "Date ABA first began",
            "Prior Applied Behavioral Health Agencies",])

        if table is None:
            return {}

        

        field_labels = {
            "service_initiation_date": [
                "Service Initiation Date",
                "Service Start Date",
                "Start Date",
            ],
            "aba_first_began": [
                "Date ABA first began",
                "ABA Start Date",
                "Date ABA Began",
            ],
            "prior_aba_agencies": [
                "Prior Applied Behavioral Health Agencies",
                "Prior ABA Agencies",
                "Previous ABA Agencies",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        service_history = {}

        for field_name, aliases in field_labels.items():
            service_history[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return service_history

    def extract_administrative_contact(self):
        table = self.find_table([
            "Administrative Contact for Current Authorization Request",
            "Full Name and Title",
            "Name and Title",
        ])

        if table is None:
            return {}

        field_labels = {
            "full_name_title": [
                "Full Name and Title",
                "Name and Title",
                "Administrative Contact",
            ],
            "phone_number": [
                "Phone Number",
                "Phone",
                "Contact Number",
            ],
            "fax_number": [
                "Fax Number",
                "Fax",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        administrative_contact = {}

        for field_name, aliases in field_labels.items():
            administrative_contact[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return administrative_contact

    def extract_chief_complaint(self):
        table = self.find_table([
            "Chief Complaint/Reason for Seeking Applied Behavior Analysis (ABA) Treatment",
            "Chief Complaint",
            "Reason for Seeking ABA Treatment",
            "Reason for Referral",
        ])

        if table is None:
            return {}

        field_labels = {
            "chief_complaint": [
                "Chief Complaint/Reason for Seeking Applied Behavior Analysis (ABA) Treatment",
                "Chief Complaint",
                "Reason for Seeking ABA Treatment",
                "Reason for Referral",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        chief_complaint = {}

        for field_name, aliases in field_labels.items():
            chief_complaint[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return chief_complaint

    def extract_records_reviewed(self):
        table = self.find_table([
            "Record Type",
            "Author of Record",
            "Date of Record",
            "Records Reviewed",])

        if table is None:
            return []
        

        records = []

        for row in table:
            # Skip rows that don't contain enough columns
            if len(row) < 3:
                continue

            record_type = row[0].strip()
            author = row[1].strip()
            date = row[2].strip()

            # Skip merged title rows where every column contains the same text
            non_empty_values = [
                cell.strip()
                for cell in row
                if cell.strip()
            ]

            if (
                non_empty_values
                and len(set(non_empty_values)) == 1
            ):
                continue

            # Skip the column header row
            if self.normalize_label(record_type) == "record type":
                continue

            # Skip completely empty rows
            if not record_type and not author and not date:
                continue

            records.append({
                "record_type": record_type,
                "author": author,
                "date": date,
            })

        return records

    def extract_interviews_conducted(self):
        table = self.find_table([
            "Initial Interview/Observation",
            "Second Interview/Observation",
            "Interview/Observation",
        ])

        if table is None:
            return []

        interviews = []

        for row_index, row in enumerate(table):
            if not row:
                continue

            label = row[0].strip()

            # Find any interview/observation label
            if "interview/observation" not in label.lower():
                continue

            # Remove instructions after the colon
            observation_type = label.split(":")[0].strip()

            # Get the narrative from the following row
            if row_index + 1 < len(table):
                next_row = table[row_index + 1]

                description = next(
                    (
                        cell.strip()
                        for cell in next_row
                        if cell.strip()
                    ),
                    None
                )

                if description:
                    interviews.append({
                        "observation_type": observation_type,
                        "description": description,
                    })

        return interviews

    def extract_individual_description(self):
        table = self.find_table([
            "Individual Description/Living Arrangements",
            "Individual Description",
            "Living Arrangements",
        ])

        if table is None:
            return {}

        field_labels = {
            "individual_description_living_arrangements": [
                "Individual Description/Living Arrangements",
                "Individual Description",
                "Living Arrangements",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        individual_description = {}

        for field_name, aliases in field_labels.items():
            individual_description[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return individual_description

    def extract_significant_medical_history(self):
        table = self.find_table([
            "Significant Medical History",
            "Medical History",
        ])

        if table is None:
            return {}

        field_labels = {
            "significant_medical_history": [
                "Significant Medical History",
                "Medical History",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        medical_history = {}

        for field_name, aliases in field_labels.items():
            medical_history[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return medical_history

    def extract_functional_communication_skills(self):
        table = self.find_table([
            "Functional Communication Skills",
            "Communication Skills",
        ])

        if table is None:
            return {}

        field_labels = {
            "functional_communication_skills": [
                "Functional Communication Skills",
                "Communication Skills",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        communication_skills = {}

        for field_name, aliases in field_labels.items():
            communication_skills[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return communication_skills

    def extract_self_care_adls(self):
        table = self.find_table([
            "Self-Care and Activities of Daily Living Skills",
            "Self-Care/ADLs",
            "Self-Care",
            "Activities of Daily Living",
            "ADLs",
        ])

        if table is None:
            return {}

        field_labels = {
            "self_care_adls": [
                "Self-Care and Activities of Daily Living Skills",
                "Self-Care/ADLs",
                "Self-Care",
                "Activities of Daily Living",
                "ADLs",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        self_care = {}

        for field_name, aliases in field_labels.items():
            self_care[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return self_care

    def extract_social_play_skills(self):
        table = self.find_table([
            "Social and Play Skills",
            "Social/Play Skills",
            "Social Skills",
            "Play Skills",
        ])

        if table is None:
            return {}

        field_labels = {
            "social_play_skills": [
                "Social and Play Skills",
                "Social/Play Skills",
                "Social Skills",
                "Play Skills",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        social_play_skills = {}

        for field_name, aliases in field_labels.items():
            social_play_skills[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return social_play_skills

    def extract_mobility_functioning_restrictions(self):
        table = self.find_table([
            "Mobility Functioning and Restrictions",
            "Mobility Functioning",
            "Mobility Restrictions",
            "Mobility",
        ])

        if table is None:
            return {}

        field_labels = {
            "mobility_functioning_restrictions": [
                "Mobility Functioning and Restrictions",
                "Mobility Functioning",
                "Mobility Restrictions",
                "Mobility",
            ],
        }

        all_labels = []

        for aliases in field_labels.values():
            all_labels.extend(aliases)

        mobility = {}

        for field_name, aliases in field_labels.items():
            mobility[field_name] = self.find_value_after_labels(
                table,
                aliases,
                all_labels
            )

        return mobility

    def extract_daily_schedule(self):
        table = self.find_table([
            "Daily schedule of all activities",
            "Daily Schedule",
            "Daily Routine",
        ])

        if table is None:
            return {}

        schedule = {}

        days = {
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        }

        for row_index, row in enumerate(table):
            normalized_row = [
                self.normalize_label(cell)
                for cell in row
            ]

            # Find the row containing the days of the week
            if any(cell in days for cell in normalized_row):

                # Schedule information should be in the next row
                if row_index + 1 >= len(table):
                    break

                activity_row = table[row_index + 1]

                for column_index, day in enumerate(row):
                    day_name = self.normalize_label(day)

                    if day_name in days:
                        value = ""

                        if column_index < len(activity_row):
                            value = activity_row[column_index].strip()

                        schedule[day_name] = value

                break

        return schedule
    
    def extract_daily_school_schedule(self):
        table = self.find_table([
            "Daily School Schedule",
            "School Schedule",
        ])

        if table is None:
            return {}

        schedule = {}

        days = {
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        }

        for row_index, row in enumerate(table):
            normalized_row = [
                self.normalize_label(cell)
                for cell in row
            ]

            # Find the row containing the days of the week
            if any(cell in days for cell in normalized_row):

                if row_index + 1 >= len(table):
                    break

                activity_row = table[row_index + 1]

                for column_index, day in enumerate(row):
                    day_name = self.normalize_label(day)

                    if day_name in days:
                        value = ""

                        if column_index < len(activity_row):
                            value = activity_row[column_index].strip()

                        schedule[day_name] = value

                break

        return schedule

    def extract_school_iep_information(self):
        table = self.find_table([
            "Are ABA services being requested for authorization from CalOptima Health at the school setting?",
            "Does the member have a current Individualized Educational Plan",
        ])

        if table is None:
            return {}

        field_labels = {
            "aba_services_requested_at_school": [
                "Are ABA services being requested for authorization from CalOptima Health at the school setting?",
            ],
            "has_current_iep": [
                "Does the member have a current Individualized Educational Plan (IEP/equivalent)?",
            ],
            "no_iep_explanation": [
                "If No, please explain",
            ],
            "aba_provider_obtained_iep": [
                "If yes, did the ABA provider obtain the current IEP/equivalent?",
            ],
            "current_iep_date": [
                "Date of the current IEP/equivalent",
            ],
            "aba_provider_participated_in_iep": [
                "Did the ABA provider participate in the IEP/equivalent meeting(s)?",
            ],
            "iep_attendance_dates": [
                "If yes, please indicate the date(s) of attendance",
            ],
            "iep_states_need_for_aba": [
                "Does the IEP/equivalent state the need for BHT/ABA services?",
            ],
        }

        school_iep = {}

        # Extract normal text values first
        for field_name, aliases in field_labels.items():
            value = None

            for row in table:
                if len(row) < 2:
                    continue

                label_cell = self.normalize_label(row[0])

                for alias in aliases:
                    normalized_alias = self.normalize_label(alias)

                    if (
                        label_cell == normalized_alias
                        or label_cell.startswith(normalized_alias + ":")
                    ):
                        value = row[1].strip()
                        break

                if value is not None:
                    break

            if value is not None:
                normalized_value = self.normalize_label(value)

                if any(
                    normalized_value == self.normalize_label(alias)
                    for alias in aliases
                ):
                    value = None

            school_iep[field_name] = value

        
        # Replaced Yes/No text with dynamically located Word checkboxes
        if self.docx_extractor is not None:
            school_iep["aba_services_requested_at_school"] = (
                self.docx_extractor.get_yes_no_checkbox_by_label([
                    "Are ABA services being requested for authorization from CalOptima Health at the school setting?"
                ])
            )

            school_iep["has_current_iep"] = (
                self.docx_extractor.get_yes_no_checkbox_by_label([
                    "Does the member have a current Individualized Educational Plan (IEP/equivalent)?"
                ])
            )

            school_iep["aba_provider_obtained_iep"] = (
                self.docx_extractor.get_yes_no_checkbox_by_label([
                    "If yes, did the ABA provider obtain the current IEP/equivalent?"
                ])
            )

            school_iep["aba_provider_participated_in_iep"] = (
                self.docx_extractor.get_yes_no_checkbox_by_label([
                    "Did the ABA provider participate in the IEP/equivalent meeting(s)?"
                ])
            )

            school_iep["iep_states_need_for_aba"] = (
                self.docx_extractor.get_yes_no_checkbox_by_label([
                    "Does the IEP/equivalent state the need for BHT/ABA services?"
                ])
            )

        return school_iep

    def extract_iep_services(self):
        table = self.find_table([
            "Individualized Educational Plan (IEP/equivalent) Information",
            "Service Type",
        ])

        if table is None:
            return []

        services = []

        expected_headers = {
            "service type",
            "location / name of school",
            "classroom type",
            "start date",
            "end date",
            "frequency",
        }

        header_row_index = None

        # Dynamically find the column-header row
        for row_index, row in enumerate(table):
            normalized_row = {
                self.normalize_label(cell)
                for cell in row
                if cell.strip()
            }

            if "service type" in normalized_row:
                header_row_index = row_index
                break

        if header_row_index is None:
            return []

        headers = table[header_row_index]

        # Map each column based on its header instead of fixed positions
        column_map = {}

        for column_index, header in enumerate(headers):
            normalized_header = self.normalize_label(header)

            if normalized_header in expected_headers:
                column_map[normalized_header] = column_index

        # Process all rows underneath the header
        for row in table[header_row_index + 1:]:

            values = {}

            for header, column_index in column_map.items():
                if column_index < len(row):
                    values[header] = row[column_index].strip()
                else:
                    values[header] = ""

            # Ignore completely empty service rows
            if not any(values.values()):
                continue

            services.append({
                "service_type": values.get("service type", ""),
                "location_school": values.get(
                    "location / name of school", ""
                ),
                "classroom_type": values.get("classroom type", ""),
                "start_date": values.get("start date", ""),
                "end_date": values.get("end date", ""),
                "frequency": values.get("frequency", ""),
            })

        return services


    def extract_previous_interventions(self):
        table = self.find_table([
            "PREVIOUS INTERVENTIONS",
            "Name of Provider",
        ])

        if table is None:
            return []

        expected_headers = {
            "name of provider",
            "service provided",
            "service level",
            "start date",
            "end date",
            "reason for termination",
        }

        header_row_index = None

        # Dynamically find the header row
        for row_index, row in enumerate(table):
            normalized_row = {
                self.normalize_label(cell)
                for cell in row
                if cell.strip()
            }

            if "name of provider" in normalized_row:
                header_row_index = row_index
                break

        if header_row_index is None:
            return []

        # Dynamically map column names to their positions
        column_map = {}

        for column_index, header in enumerate(table[header_row_index]):
            normalized_header = self.normalize_label(header)

            if normalized_header in expected_headers:
                column_map[normalized_header] = column_index

        interventions = []

        # Extract every populated row after the headers
        for row in table[header_row_index + 1:]:
            values = {}

            for header, column_index in column_map.items():
                if column_index < len(row):
                    values[header] = row[column_index].strip()
                else:
                    values[header] = ""

            if not any(values.values()):
                continue

            interventions.append({
                "provider_name": values.get("name of provider", ""),
                "service_provided": values.get("service provided", ""),
                "service_level": values.get("service level", ""),
                "start_date": values.get("start date", ""),
                "end_date": values.get("end date", ""),
                "reason_for_termination": values.get(
                    "reason for termination", ""
                ),
            })

        return interventions

    def extract_coordination_of_care(self):
        table = self.find_table([
            "Parent/Caregiver",
            "Regional Center",
            "Mental Health Provider",
        ])

        if table is None:
            return {}

        field_labels = {
            "parent_caregiver": [
                "Parent/Caregiver",
                "Parent / Caregiver",
            ],
            "school": [
                "School",
            ],
            "regional_center": [
                "Regional Center",
            ],
            "speech_ot_pt": [
                "Speech/OT/PT",
                "Speech / OT / PT",
            ],
            "primary_care_provider_specialist": [
                "Primary Care Provider/Specialist",
                "Primary Care Provider / Specialist",
                "PCP/Specialist",
            ],
            "mental_health_provider": [
                "Mental Health Provider",
            ],
        }

        coordination = {}

        for field_name, aliases in field_labels.items():
            value = self.find_value_after_labels(
                table,
                aliases,
                [
                    label
                    for alias_list in field_labels.values()
                    for label in alias_list
                ]
            )

            coordination[field_name] = value

        return coordination


    def extract_adaptive_testing(self):
        table = self.find_table([
            "Vineland-3 Scoring Information",
            "Date Administered",
            "Facilitated By",
        ])

        if table is None:
            return {}

        result = {
            "assessment": "Vineland-3",
            "baseline": {},
            "current": {},
            "scores": [],
        }

        baseline_columns = []
        current_columns = []
        score_header_row = None

        # Find Baseline / Current column groups and score header row
        for row_index, row in enumerate(table):
            normalized_row = [
                self.normalize_label(cell)
                for cell in row
            ]

            if "baseline" in normalized_row or "current" in normalized_row:
                baseline_columns = [
                    index
                    for index, value in enumerate(normalized_row)
                    if value == "baseline"
                ]

                current_columns = [
                    index
                    for index, value in enumerate(normalized_row)
                    if value == "current"
                ]

            if "domain" in normalized_row:
                score_header_row = row_index
                break

        if score_header_row is None:
            return result

        # Assessment metadata
        for row in table[:score_header_row]:
            if not row:
                continue

            label = self.normalize_label(row[0])

            if label == "date administered":
                if baseline_columns:
                    result["baseline"]["date_administered"] = (
                        row[baseline_columns[0]].strip()
                    )

                if current_columns:
                    result["current"]["date_administered"] = (
                        row[current_columns[0]].strip()
                    )

            elif label == "facilitated by":
                if baseline_columns:
                    result["baseline"]["facilitated_by"] = (
                        row[baseline_columns[0]].strip()
                    )

                if current_columns:
                    result["current"]["facilitated_by"] = (
                        row[current_columns[0]].strip()
                    )

            elif label == "respondent":
                if baseline_columns:
                    result["baseline"]["respondent"] = (
                        row[baseline_columns[0]].strip()
                    )

                if current_columns:
                    result["current"]["respondent"] = (
                        row[current_columns[0]].strip()
                    )

        # Score rows
        current_domain = None

        for row in table[score_header_row + 1:]:
            if not row:
                continue

            name = row[0].strip()

            if not name:
                continue

            remaining_values = [
                cell.strip()
                for cell in row[1:]
            ]

            # Domain heading rows have no scores
            if not any(remaining_values):
                current_domain = name
                continue

            baseline_raw = row[1].strip() if len(row) > 1 else ""
            baseline_standard = row[2].strip() if len(row) > 2 else ""
            baseline_age = row[3].strip() if len(row) > 3 else ""

            current_raw = row[4].strip() if len(row) > 4 else ""
            current_standard = row[5].strip() if len(row) > 5 else ""
            current_age = row[6].strip() if len(row) > 6 else ""

            result["scores"].append({
                "domain": current_domain,
                "skill_area": name,
                "baseline": {
                    "raw_score": baseline_raw,
                    "standard_v_scale_score": baseline_standard,
                    "age_equivalent": baseline_age,
                },
                "current": {
                    "raw_score": current_raw,
                    "standard_v_scale_score": current_standard,
                    "age_equivalent": current_age,
                },
            })

        return result

    def extract_diagnostic_information(self):
        table = self.find_table([
            "DIAGNOSTIC INFORMATION",
            "Current diagnosis code",
            "Diagnosis description",
        ])

        if table is None:
            return []

        header_aliases = {
            "diagnosis_code": [
                "Current diagnosis code",
                "Diagnosis code",
                "ICD code",
            ],
            "diagnosis_description": [
                "Diagnosis description",
                "Diagnosis",
            ],
            "diagnosis_date": [
                "Date of diagnosis/report",
                "Date of diagnosis",
                "Diagnosis date",
            ],
            "diagnosed_by": [
                "Diagnosed by (Full Name & credential)",
                "Diagnosed by",
            ],
        }

        header_row_index = None
        column_map = {}

        # Dynamically locate the header row
        for row_index, row in enumerate(table):
            temporary_map = {}

            for column_index, cell in enumerate(row):
                normalized_cell = self.normalize_label(cell)

                for field_name, aliases in header_aliases.items():
                    normalized_aliases = {
                        self.normalize_label(alias)
                        for alias in aliases
                    }

                    if normalized_cell in normalized_aliases:
                        temporary_map[field_name] = column_index
                        break

            # Require at least the diagnosis code and description
            if (
                "diagnosis_code" in temporary_map
                and "diagnosis_description" in temporary_map
            ):
                header_row_index = row_index
                column_map = temporary_map
                break

        if header_row_index is None:
            return []

        diagnoses = []

        # Extract all diagnosis rows below the headers
        for row in table[header_row_index + 1:]:
            diagnosis = {}

            for field_name, column_index in column_map.items():
                if column_index < len(row):
                    diagnosis[field_name] = row[column_index].strip()
                else:
                    diagnosis[field_name] = ""

            # Ignore completely empty rows
            if not any(diagnosis.values()):
                continue

            diagnoses.append(diagnosis)

        return diagnoses

    def extract_functional_assessments(self):
        table = self.find_table([
            "FUNCTIONAL ASSESSMENT OR ANALYSIS OF TARGET BEHAVIORS",
            "Target Behavior",
        ])

        if table is None:
            return []

        field_labels = {
            "operational_definition": [
                "Operational Definition",
            ],
            "course_of_behavior": [
                "Course of Behavior",
            ],
            "baseline_data": [
                "Baseline Data",
            ],
            "history_problem_chief_complaint": [
                "History of the Problem/Chief Complaint",
                "History of the Problem",
            ],
            "setting_events": [
                "Setting Events",
            ],
            "trigger_events": [
                "Trigger Events",
            ],
            "consequent_analysis": [
                "Consequent Analysis",
            ],
            "hypothesized_function": [
                "Impressions and Analysis of Hypothesized Function",
                "Hypothesized Function",
            ],
        }

        assessments = []
        current_assessment = None

        for row_index, row in enumerate(table):
            if not row:
                continue

            first_cell = row[0].strip()
            normalized_first_cell = self.normalize_label(first_cell)

            # Dynamically detect Target Behavior 1, 2, 3, etc.
            if normalized_first_cell.startswith("target behavior"):
                behavior_name = ""

                # Usually the behavior name is in the next column
                if len(row) > 1:
                    behavior_name = row[1].strip()

                current_assessment = {
                    "target_behavior": behavior_name,
                }

                assessments.append(current_assessment)
                continue

            if current_assessment is None:
                continue

            # Match each assessment field dynamically
            for field_name, aliases in field_labels.items():
                matched = False

                for alias in aliases:
                    normalized_alias = self.normalize_label(alias)

                    if (
                        normalized_first_cell == normalized_alias
                        or normalized_first_cell.startswith(
                            normalized_alias + ":"
                        )
                        or normalized_first_cell.startswith(
                            normalized_alias + " "
                        )
                    ):
                        matched = True
                        break

                if not matched:
                    continue

                value = ""

                # In this template the value follows the label row.
                if row_index + 1 < len(table):
                    next_row = table[row_index + 1]

                    # Merged cells can repeat the same value,
                    # so take the first populated cell.
                    value = next(
                        (
                            cell.strip()
                            for cell in next_row
                            if cell.strip()
                        ),
                        "",
                    )

                current_assessment[field_name] = value
                break

        return assessments

    def extract_behavior_intervention_plans(self):
        table = self.find_table([
            "BEHAVIOR INTERVENTION PLAN",
            "Ecological interventions",
            "Training of replacement behaviors",
        ])

        if table is None:
            return []

        field_labels = {
            "ecological_interventions": [
                "Ecological interventions",
            ],
            "replacement_behavior_training": [
                "Training of replacement behaviors",
                "Replacement behavior training",
            ],
            "focused_intervention_strategies": [
                "Focused intervention strategies",
            ],
            "reactive_strategies": [
                "Reactive Strategies",
            ],
            "data_collection_procedures": [
                "Data collection procedures",
            ],
        }

        plans = []
        current_plan = None

        for row_index, row in enumerate(table):
            if not row:
                continue

            first_cell = row[0].strip()
            normalized_first = self.normalize_label(first_cell)

            # Detect Target Behavior 1, 2, 3, etc.
            if normalized_first.startswith("target behavior"):
                target_behavior = ""

                if len(row) > 1:
                    target_behavior = row[1].strip()

                current_plan = {
                    "target_behavior": target_behavior,
                }

                plans.append(current_plan)
                continue

            if current_plan is None:
                continue

            for field_name, aliases in field_labels.items():
                matched = False

                for alias in aliases:
                    normalized_alias = self.normalize_label(alias)

                    if (
                        normalized_first == normalized_alias
                        or normalized_first.startswith(
                            normalized_alias + ":"
                        )
                        or normalized_first.startswith(
                            normalized_alias + " "
                        )
                    ):
                        matched = True
                        break

                if not matched:
                    continue

                value = ""

                # Content follows the label row
                if row_index + 1 < len(table):
                    next_row = table[row_index + 1]

                    value = next(
                        (
                            cell.strip()
                            for cell in next_row
                            if cell.strip()
                        ),
                        "",
                    )

                current_plan[field_name] = value
                break

        return plans


    def extract_mediator_analysis(self):
        table = self.find_table([
            "MEDIATOR ANALYSIS",
            "Mediator Analysis",
        ])

        if table is None:
            return {}

        # Find the Mediator Analysis heading dynamically
        for row_index, row in enumerate(table):
            for cell in row:
                if self.normalize_label(cell) == "mediator analysis":

                    # Search the rows after the heading.
                    # Skip the instruction row and return the
                    # first populated narrative row.
                    for next_row in table[row_index + 1:]:
                        non_empty_values = [
                            value.strip()
                            for value in next_row
                            if value.strip()
                        ]

                        if not non_empty_values:
                            continue

                        value = non_empty_values[0]

                        # Skip the template instruction
                        if value.lower().startswith(
                            "provide additional information"
                        ):
                            continue

                        return {
                            "mediator_analysis": value
                        }

        return {}

    def extract_reinforcer_assessment(self):
        table = self.find_table([
            "REINFORCER ASSESSMENT",
            "Reinforcer Assessment",
        ])

        if table is None:
            return {}

        # Dynamically locate the Reinforcer Assessment heading
        for row_index, row in enumerate(table):
            for cell in row:
                if self.normalize_label(cell) == "reinforcer assessment":

                    # Search all rows following the heading
                    for next_row in table[row_index + 1:]:
                        non_empty_values = [
                            value.strip()
                            for value in next_row
                            if value.strip()
                        ]

                        if not non_empty_values:
                            continue

                        value = non_empty_values[0]

                        # Skip template instruction text
                        if value.lower().startswith(
                            "describe reinforcers identified"
                        ):
                            continue

                        return {
                            "reinforcer_assessment": value
                        }

        return {}

    def extract_target_replacement_goals(self):
        target_goals = []
        replacement_goals = []

        # Keep current_goal outside the table loop so a goal
        # can continue into the next Word table.
        current_goal = None

        for table in self.tables:

            for row_index, row in enumerate(table):
                if not row:
                    continue

                first_value = next(
                    (
                        cell.strip()
                        for cell in row
                        if cell.strip()
                    ),
                    "",
                )

                if not first_value:
                    continue

                normalized_value = self.normalize_label(first_value)

                # -------------------------
                # TARGET BEHAVIOR GOAL
                # -------------------------
                if normalized_value.startswith("target behavior goal"):
                    current_goal = {
                        "goal": first_value,
                        "topography": "",
                        "location_setting": "",
                        "antecedent_strategies": "",
                        "consequent_strategies": "",
                        "date_of_introduction": "",
                        "baseline_data_date": "",
                    }

                    target_goals.append(current_goal)
                    continue

                # -------------------------
                # REPLACEMENT BEHAVIOR GOAL
                # -------------------------
                if normalized_value.startswith("replacement behavior goal"):
                    current_goal = {
                        "goal": first_value,
                        "date_of_introduction": "",
                        "location_setting": "",
                        "baseline_data_date": "",
                    }

                    replacement_goals.append(current_goal)
                    continue

                if current_goal is None:
                    continue

                # -------------------------
                # TARGET GOAL FIELDS
                # -------------------------
                if normalized_value.startswith(
                    "topography of target behavior"
                ):
                    current_goal["topography"] = first_value

                elif normalized_value.startswith(
                    "antecedent strategies for target behavior"
                ):
                    current_goal["antecedent_strategies"] = first_value

                elif normalized_value.startswith(
                    "consequent strategies for target behavior"
                ):
                    current_goal["consequent_strategies"] = first_value

                # -------------------------
                # DATE OF INTRODUCTION
                # -------------------------
                elif normalized_value.startswith("date of introduction"):
                    current_goal["date_of_introduction"] = first_value

                # Handles things like:
                # "1.Date of Introduction: August 2025"
                elif (
                    "date of introduction" in normalized_value
                    and normalized_value[0].isdigit()
                ):
                    current_goal["date_of_introduction"] = first_value

                # -------------------------
                # BASELINE
                # -------------------------
                elif normalized_value.startswith(
                    "baseline data and date"
                ):
                    current_goal["baseline_data_date"] = first_value

                # -------------------------
                # LOCATION / SETTING
                # -------------------------
                elif (
                    normalized_value.startswith(
                        "location/setting of target behavior"
                    )
                    or normalized_value.startswith(
                        "location/setting of replacement behavior"
                    )
                ):
                    location = ""

                    # Location choices are in the following row
                    if row_index + 1 < len(table):
                        next_row = table[row_index + 1]

                        location = next(
                            (
                                cell.strip()
                                for cell in next_row
                                if cell.strip()
                            ),
                            "",
                        )

                    current_goal["location_setting"] = location

        return {
            "target_behavior_goals": target_goals,
            "replacement_behavior_goals": replacement_goals,
        }

        