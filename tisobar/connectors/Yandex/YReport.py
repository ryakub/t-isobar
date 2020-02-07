import requests, json, time


class YandexReport:
    def __init__(self, access_token, client_login):
        self.url = "https://api.direct.yandex.com/json/v5/reports"
        self.headers_report = {
            "Authorization": "Bearer " + access_token,
            "Client-Login": client_login,
            "Accept-Language": "ru",
            "processingMode": "auto",
            "returnMoneyInMicros": "false",
            "skipReportHeader": "true",
            "skipReportSummary": "true"}

    def create_body(self, selection_criteria, field_names, report_name, report_type):
        body = {
            "params": {
                "SelectionCriteria": selection_criteria,
                "FieldNames": field_names,
                "ReportName": (report_name),
                "ReportType": report_type,
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "NO",
                "IncludeDiscount": "NO"
            }
        }
        json_body = json.dumps(body, ensure_ascii=False).encode('utf8')
        return json_body

    def request(self, selection_criteria, field_names, report_name, report_type):
        json_body = self.create_body(selection_criteria, field_names, report_name, report_type)
        data = requests.post(self.url, json_body, headers=self.headers_report)
        if data.status_code in [201, 202]:
            time.sleep(60)
            return self.request(selection_criteria, field_names, report_name, report_type)
        return data

    def get_report(self, report_type, report_name, date_from, date_to, fields=[]):
        """
        report_name - report_type - fields:
         - CUSTOM_LOCATION_REPORT - CUSTOM_REPORT - ["TargetingLocationId", "TargetingLocationName"]
         - CUSTOM_PLACEMENT_REPORT - CUSTOM_REPORT - ["Placement"]
         - CUSTOM_GENDER_REPORT - CUSTOM_REPORT - ["Age", "Device", "Gender"]
         - SEARCH_QUERY_PERFORMANCE_REPORT - SEARCH_QUERY_PERFORMANCE_REPORT - ["Criterion", "CriterionId",
         "CriteriaType"]

         date format: "YYYY-MM-DD"

        """
        selection_criteria = {"DateFrom": date_from, "DateTo": date_to}
        field_names = ["AdId", "CampaignId", "CampaignName", "CampaignType", "AdGroupId", "AdGroupName", "Date",
                       "Clicks", "Cost", "Impressions"] + fields
        data = self.request(selection_criteria, field_names, report_name, report_type)
        return data
