from zipfile import ZipFile
from pathlib import Path
from xml.etree import ElementTree as ET
import json

docx_path = Path("documents/fba.docx")

namespaces = {
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart"
}

charts = []

with ZipFile(docx_path, "r") as docx:

    chart_files = [
        name for name in docx.namelist()
        if name.startswith("word/charts/chart")
        and name.endswith(".xml")
    ]

    for chart_file in chart_files:
        root = ET.fromstring(docx.read(chart_file))

        for series in root.findall(".//c:ser", namespaces):

            categories = {}
            values = {}

            for point in series.findall(".//c:cat//c:pt", namespaces):
                index = int(point.get("idx"))
                value = point.find("c:v", namespaces)

                if value is not None and value.text:
                    categories[index] = value.text.strip()

            for point in series.findall(".//c:val//c:pt", namespaces):
                index = int(point.get("idx"))
                value = point.find("c:v", namespaces)

                if value is not None and value.text:
                    values[index] = float(value.text)

            scores = {
                categories[index]: (
                    int(value) if value.is_integer() else value
                )
                for index, value in values.items()
                if index in categories
            }

            charts.append({
                "chart_file": chart_file,
                "scores": scores
            })

print("\n========== EXTRACTED CHART DATA ==========")
print(json.dumps(charts, indent=4))