from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import MedicalReport
from .serializers import MedicalReportSerializer
from django.contrib.auth.models import User
from .utils import call_deepseek_ai
from .utils import format_table_for_ai
import requests
import time
import os


# 🔹 Azure OCR Call
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")
print("🔐 AZURE_ENDPOINT =", os.getenv("AZURE_ENDPOINT"))
def call_azure_ocr(file):
    url = f"{AZURE_ENDPOINT}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2023-07-31"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }

    file.seek(0)
    response = requests.post(url, headers=headers, data=file.read())

    if response.status_code != 202:
        raise Exception("Azure OCR failed", response.text)

    result_url = response.headers["operation-location"]

    # Polling
    for _ in range(10):
        time.sleep(1)
        result = requests.get(result_url, headers={"Ocp-Apim-Subscription-Key": AZURE_KEY})
        result_json = result.json()
        if result_json.get("status") == "succeeded":
            return result_json  # NOT just analyzeResult
    raise Exception("Azure OCR polling timed out")


# 🔹 Extract Tables and Date
def extract_tables_and_date(ocr_json):
    result = {}
    analyze_result = ocr_json.get("analyzeResult", {})

    # Extract Tables
    tables = analyze_result.get("tables", [])
    parsed_tables = []
    for table in tables:
        rows = table.get("rowCount", 0)
        cols = table.get("columnCount", 0)
        cells = table.get("cells", [])
        data_grid = [["" for _ in range(cols)] for _ in range(rows)]

        for cell in cells:
            row = cell.get("rowIndex")
            col = cell.get("columnIndex")
            text = cell.get("content", "")
            data_grid[row][col] = text

        parsed_tables.append(data_grid)

    result["tables"] = parsed_tables

    # Extract Report Date
    for kv in analyze_result.get("keyValuePairs", []):
        key = kv.get("key", {}).get("content", "").lower()
        val = kv.get("value", {}).get("content", "")
        if "date" in key and val:
            result["report_date"] = val
            break

    return result


# 🔹 Upload View
class UploadLabReport(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print("🔍 Raw request data:", request.data)

        user = User.objects.first()  # TEMP: Replace with actual auth
        file = request.data.get("original_file")
        report_type = request.data.get("report_type")

        if not file or not report_type:
            return Response({"error": "File and report_type are required."}, status=400)

        # Step 1: Save file to DB (first)
        report = MedicalReport.objects.create(
            user=user,
            report_type=report_type,
            original_file=file
        )

        try:
            # Step 2: OCR Call + Cleanup
            print("🚀 Starting OCR processing...")
            ocr_json = call_azure_ocr(file)
            print("✅ OCR processing completed successfully.")

            cleaned_data = extract_tables_and_date(ocr_json)
            print("🧹 Cleaned data:", cleaned_data)

            ai_prompt = format_table_for_ai(cleaned_data)
            print("📋 AI prompt ready.")

            from datetime import datetime
            raw_date = cleaned_data.get("report_date", "")
            print("📅 Raw date:", raw_date)
            parsed_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    parsed_date = datetime.strptime(raw_date, fmt).date()
                    print("✅ Parsed date:", parsed_date)
                    break
                except Exception as e :
                    print(f"❌ Date parse failed for format {fmt}: {e}")
            
            # Step 3: Save extracted data to model
            report.extracted_data = cleaned_data
            report.ai_prompt_preview = ai_prompt
            report.report_date = parsed_date
            report.save()
            print("✅ Report saved after OCR.")

            try:
            #call AI service
             ai_summary = call_deepseek_ai(ai_prompt)
             report.ai_summary = ai_summary
             report.save()
             print("✅ AI summary saved to report.")

            

            except Exception as ai_err:
                print("❌ AI call failed:", ai_err)
            
            
            return Response({"message": "Report uploaded and processed successfully.", "ai_summary": ai_summary}, status=201)
        except Exception as e:
            print("🔥 Outer exception:", e)
            return Response({"error": str(e)}, status=500)

# user ki saari reports ko fetch karne ke liye
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MedicalReport
from .serializers import MedicalReportSerializer
from rest_framework import status
class ReportListAPIView(APIView):
    def get(self, request):
        reports = MedicalReport.objects.all().order_by('-report_date')
        serializer = MedicalReportSerializer(reports, many=True)
        return Response(serializer.data)

class ReportDeleteView(APIView):
    def delete(self, request, pk):
        try:
            report = MedicalReport.objects.get(pk=pk)
            report.delete()
            return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MedicalReport.DoesNotExist:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
