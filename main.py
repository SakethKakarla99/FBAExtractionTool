from src.docx_extractor import *
from src.fba_extractor import *


FILE_PATH = "documents/fba.docx"

docx_extractor = DOCXExtractor(FILE_PATH)

tables = docx_extractor.get_tables()

fba_extractor = FBAExtractor(tables, docx_extractor)

identification = fba_extractor.extract_identification()

print("\n========== IDENTIFICATION ==========")

for key, value in identification.items():
    print(f"{key}: {value}")

service_history = fba_extractor.extract_service_history()

print("\n========== SERVICE HISTORY ==========")

for key, value in service_history.items():
    print(f"{key}: {value}")

administrative_contact = fba_extractor.extract_administrative_contact()

print("\n========== ADMINISTRATIVE CONTACT ==========")

for key, value in administrative_contact.items():
    print(f"{key}: {value}")

chief_complaint = fba_extractor.extract_chief_complaint()

print("\n========== CHIEF COMPLAINT ==========")

for key, value in chief_complaint.items():
    print(f"{key}: {value}")


records_reviewed = fba_extractor.extract_records_reviewed()
print("\n========== RECORDS REVIEWED ==========")

for record in records_reviewed:
    print(f"Record Type: {record['record_type']}")
    print(f"Author: {record['author']}")
    print(f"Date: {record['date']}")
    print()

interviews_conducted = fba_extractor.extract_interviews_conducted()

print("\n========== INTERVIEWS CONDUCTED ==========")

for interview in interviews_conducted:
    print(interview)


individual_description = fba_extractor.extract_individual_description()

print("\n========== INDIVIDUAL DESCRIPTION ==========")
print(individual_description)

medical_history = fba_extractor.extract_significant_medical_history()

print("\n========== SIGNIFICANT MEDICAL HISTORY ==========")
print(medical_history)

communication_skills = fba_extractor.extract_functional_communication_skills()

print("\n========== FUNCTIONAL COMMUNICATION SKILLS ==========")
print(communication_skills)

self_care_adls = fba_extractor.extract_self_care_adls()

print("\n========== SELF-CARE / ADLS ==========")
print(self_care_adls)

social_play_skills = fba_extractor.extract_social_play_skills()

print("\n========== SOCIAL AND PLAY SKILLS ==========")
print(social_play_skills)

mobility = fba_extractor.extract_mobility_functioning_restrictions()
print("\n========== MOBILITY FUNCTIONING AND RESTRICTIONS ==========")
print(mobility)

daily_schedule = fba_extractor.extract_daily_schedule()

print("\n========== DAILY SCHEDULE ==========")

for day, activity in daily_schedule.items():
    print(f"{day}: {activity}")


daily_school_schedule = fba_extractor.extract_daily_school_schedule()

print("\n========== DAILY SCHOOL SCHEDULE ==========")

for day, activity in daily_school_schedule.items():
    print(f"{day}: {activity}")


school_iep = fba_extractor.extract_school_iep_information()

print("\n========== SCHOOL / IEP INFORMATION ==========")

for field, value in school_iep.items():
    print(f"{field}: {value}")


iep_services = fba_extractor.extract_iep_services()

print("\n========== IEP SERVICES ==========")

if not iep_services:
    print("No IEP services listed.")
else:
    for service in iep_services:
        print(service)


previous_interventions = fba_extractor.extract_previous_interventions()

print("\n========== PREVIOUS INTERVENTIONS ==========")

if not previous_interventions:
    print("No previous interventions listed.")
else:
    for intervention in previous_interventions:
        print(intervention)


coordination_of_care = fba_extractor.extract_coordination_of_care()

print("\n========== COORDINATION OF CARE ==========")

for field, value in coordination_of_care.items():
    print(f"{field}: {value}")



adaptive_testing = fba_extractor.extract_adaptive_testing()

print("\n========== ADAPTIVE TESTING ==========")

print("Assessment:", adaptive_testing.get("assessment"))

print("Baseline:")
print(adaptive_testing.get("baseline"))

print("Current:")
print(adaptive_testing.get("current"))

print("Scores:")

for score in adaptive_testing.get("scores", []):
    print(score)

diagnostic_information = (fba_extractor.extract_diagnostic_information())

print("\n========== DIAGNOSTIC INFORMATION ==========")

if not diagnostic_information:
    print("No diagnostic information found.")
else:
    for diagnosis in diagnostic_information:
        print(diagnosis)



functional_assessments = (
    fba_extractor.extract_functional_assessments()
)

print("\n========== FUNCTIONAL ASSESSMENTS ==========")

if not functional_assessments:
    print("No functional assessments found.")
else:
    for assessment in functional_assessments:
        print("\nTarget Behavior:", assessment.get("target_behavior"))

        for field, value in assessment.items():
            if field != "target_behavior":
                print(f"{field}: {value}")


behavior_intervention_plans = (
    fba_extractor.extract_behavior_intervention_plans()
)

print("\n========== BEHAVIOR INTERVENTION PLANS ==========")

if not behavior_intervention_plans:
    print("No behavior intervention plans found.")
else:
    for plan in behavior_intervention_plans:
        print("\nTarget Behavior:", plan.get("target_behavior"))

        for field, value in plan.items():
            if field != "target_behavior":
                print(f"{field}: {value}")

mediator_analysis = (
    fba_extractor.extract_mediator_analysis()
)

print("\n========== MEDIATOR ANALYSIS ==========")

for field, value in mediator_analysis.items():
    print(f"{field}: {value}")

reinforcer_assessment = (
    fba_extractor.extract_reinforcer_assessment()
)

print("\n========== REINFORCER ASSESSMENT ==========")

for field, value in reinforcer_assessment.items():
    print(f"{field}: {value}")



behavior_goals = (
    fba_extractor.extract_target_replacement_goals()
)

print("\n========== TARGET BEHAVIOR GOALS ==========")

for goal in behavior_goals["target_behavior_goals"]:
    print("\n", goal)


print("\n========== REPLACEMENT BEHAVIOR GOALS ==========")

for goal in behavior_goals["replacement_behavior_goals"]:
    print("\n", goal)


skill_acquisition_goals = (
    fba_extractor.extract_skill_acquisition_goals()
)

print("\n========== SKILL ACQUISITION GOALS ==========")

for area in skill_acquisition_goals:
    print(
        f"\nIntervention Area: "
        f"{area['intervention_area']}"
    )

    for goal in area["goals"]:
        print("\n", goal)


parent_caregiver_goals = (
    fba_extractor.extract_parent_caregiver_goals()
)

print("\n========== PARENT CAREGIVER GOALS ==========")

print("\nParticipants:")
for participant in parent_caregiver_goals["participants"]:
    print(participant)

print("\nGoals:")
for goal in parent_caregiver_goals["goals"]:
    print(goal)


generalization_plan = (
    fba_extractor.extract_generalization_maintenance_plan()
)

print(
    "\n========== GENERALIZATION MAINTENANCE PLAN =========="
)

for key, value in generalization_plan.items():
    print(f"\n{key}:")
    print(value)


transition_plan = (
    fba_extractor.extract_transition_plan()
)

print("\n========== TRANSITION PLAN ==========")

for key, value in transition_plan.items():
    print(f"\n{key}:")
    print(value)

crisis_plan = (
    fba_extractor.extract_crisis_plan()
)

print("\n========== CRISIS PLAN ==========")

for key, value in crisis_plan.items():
    print(f"\n{key}:")
    print(value)

summary_recommendations = (
    fba_extractor.extract_summary_recommendations()
)

print("\n========== SUMMARY AND RECOMMENDATIONS ==========")

print("\nClinical Summary:")
print(summary_recommendations["clinical_summary"])

print("\nService Requests:")

for service in summary_recommendations["service_requests"]:
    print("\n", service)


parent_guardian_involvement = (
    fba_extractor.extract_parent_guardian_involvement()
)

print(
    "\n========== PARENT GUARDIAN INVOLVEMENT =========="
)

for key, value in parent_guardian_involvement.items():
    print(f"{key}: {value}")