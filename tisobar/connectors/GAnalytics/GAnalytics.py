import time, socket
from apiclient.discovery import build
from google.oauth2 import service_account


class GAnalytics:
    def __init__(self, path_to_json, view_id):
        self.KEY_FILE_LOCATION = path_to_json
        self.SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
        self.VIEW_ID = view_id
        self.credentials = service_account.Credentials.from_service_account_file(self.KEY_FILE_LOCATION)
        self.scoped_credentials = self.credentials.with_scopes(self.SCOPES)
        self.analytics = build('analyticsreporting', 'v4', credentials=self.scoped_credentials)

    def convert_data(self, dimension_list, metric_list, response_data_list):
        columns = dimension_list + metric_list
        total_data_list = []
        for element in response_data_list:
            for one_dict in element:
                total_data_list.append(one_dict['dimensions'] + one_dict['metrics'][0]['values'])
        return columns, total_data_list

    def request(self, body):
        try:
            response = self.analytics.reports().batchGet(body=body).execute()
        except socket.timeout:
            time.sleep(2)
            return self.request(body)
        except ConnectionResetError:
            time.sleep(2)
            self.analytics = build('analyticsreporting', 'v4', credentials=self.scoped_credentials)
            return self.request(body)
        return response

    def create_params(self, list_of_params, type_of_metric):
        params_dict = []
        if type_of_metric == "metrics":
            key = 'expression'
        elif type_of_metric == "dimensions":
            key = 'name'
        else:
            raise Exception("Not supported type")
        for param in list_of_params:
            params_dict.append({key: param})
        return params_dict

    def create_body(self, date_from, date_to, metric, dimension, page_token=''):
        body = {
            "reportRequests":
                [{
                    "viewId": self.VIEW_ID,
                    "dateRanges": [{"startDate": date_from, "endDate": date_to}],
                    "metrics": metric,
                    "dimensions": dimension,
                    "pageSize": 100000,
                    "pageToken": page_token
                }]
        }
        return body

    def get_request(self, date_from, date_to, metric_list, dimension_list):
        metric = self.create_params(metric_list, 'metrics')
        dimension = self.create_params(dimension_list, 'dimensions')
        response_data_list = []

        body = self.create_body(date_from, date_to, metric, dimension)

        response = self.request(body)
        response_data_list.append(response['reports'][0]['data']['rows'])

        while response['reports'][0].get('nextPageToken') != None:
            body = self.create_body(date_from, date_to, metric, dimension,
                                    page_token=response['reports'][0]['nextPageToken'])
            response = self.request(body)
            response_data_list.append(response['reports'][0]['data']['rows'])
            time.sleep(2)
        columns, result_list_of_data = self.convert_data(dimension_list, metric_list, response_data_list)
        return columns, result_list_of_data
