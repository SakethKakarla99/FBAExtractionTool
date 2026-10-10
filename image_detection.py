from zipfile import ZipFile
from pathlib import Path
from xml.etree import ElementTree as ET
import json

docx_path = Path("documents/fba.docx")

namespaces = {
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart"
}

def extract_chart_data(docx_path):
    charts = []

    with ZipFile(docx_path, "r") as docx:

        chart_files = [
            name for name in docx.namelist()
            if name.startswith("word/charts/chart")
            and name.endswith(".xml")
        ]

        for chart_file in chart_files:
            root = ET.fromstring(docx.read(chart_file))

            for series_index, series in enumerate(
                root.findall(".//c:ser", namespaces)
            ):
                categories = {}
                values = {}

                for point in series.findall(
                    "./c:cat//c:pt", namespaces
                ):
                    value = point.find("c:v", namespaces)

                    if value is not None and value.text:
                        categories[int(point.get("idx"))] = (
                            value.text.strip()
                        )

                for point in series.findall(
                    "./c:val//c:pt", namespaces
                ):
                    value = point.find("c:v", namespaces)

                    if value is not None and value.text:
                        values[int(point.get("idx"))] = float(
                            value.text
                        )

                scores = {
                    categories[index]: (
                        int(value)
                        if value.is_integer()
                        else value
                    )
                    for index, value in values.items()
                    if index in categories
                }

                charts.append({
                    "chart_file": chart_file,
                    "series_index": series_index,
                    "scores": scores,
                    "extraction_method": "chart_xml"
                })

    return charts


if __name__ == "__main__":

    charts = extract_chart_data(docx_path)

    print("\n========== EXTRACTED CHART DATA ==========")
    print(json.dumps(charts, indent=4))