import requests
import time
import pandas as pd


class YMLogs:
    def __init__(self, access_token, counter, date1, date2, fields, source='visits'):
        self.__access_token = access_token
        self.__request_url = f"https://api-metrika.yandex.net/management/v1/counter/{counter}/"
        self.__source = source
        self.date1 = date1
        self.date2 = date2
        self.__fields = "ym:s:visitID,ym:s:counterID,ym:s:dateTime,ym:s:isNewUser,ym:s:startURL,ym:s:endURL," \
                        "ym:s:pageViews,ym:s:visitDuration,ym:s:bounce,ym:s:regionCountry,ym:s:regionCity," \
                        "ym:s:regionCountryID,ym:s:regionCityID,ym:s:clientID,ym:s:networkType,ym:s:goalsID," \
                        "ym:s:goalsDateTime,ym:s:UTMCampaign,ym:s:UTMContent,ym:s:UTMMedium,ym:s:UTMSource," \
                        "ym:s:UTMTerm,ym:s:hasGCLID,ym:s:lastGCLID,ym:s:firstGCLID,ym:s:lastSignificantGCLID," \
                        "ym:s:deviceCategory"

    def __request(self, method, request_type, **kwargs):
        headers = {"Authorization": 'OAuth ' + self.__access_token, "Host": 'api-metrika.yandex.net',
                   'Content-Type': 'application/x-yametrika+json', 'date1': self.date1}
        params = kwargs
        if 'oauth_token' not in params:
            params['oauth_token'] = self.__access_token
        if request_type == "post":
            response = requests.post(self.__request_url + method, params=params, headers=headers)
        else:
            response = requests.get(self.__request_url + method, params=params, headers=headers)
        return response

    def evaluate(self):
        method = "logrequests/evaluate/"
        evaluate_response = self.__request(method, request_type="get", date1=self.date1, date2=self.date2,
                                           fields=self.__fields, source=self.__source).json()
        return evaluate_response

    def logrequest_id(self):
        method = "logrequests/"
        logrequest_id_response = self.__request(method, request_type="post", date1=self.date1, date2=self.date2,
                                                fields=self.__fields, source=self.__source).json()
        return logrequest_id_response['log_request']['request_id']

    def logrequests(self, request_id):
        method = f"logrequest/{request_id}"
        logrequests_response = self.__request(method, request_type="get").json()
        if logrequests_response['log_request']['status'] == 'created':
            time.sleep(30)
            return self.logrequests(request_id)
        return logrequests_response['log_request']['parts']

    def download(self, request_id, parts):
        all_data_frame = []
        for part in parts:
            part_id = part['part_number']
            method = f"logrequest/{request_id}/part/{part_id}/download/"
            download = self.__request(method, request_type="get")
            data = self.__get_data(download)
            all_data_frame.append(data)
        all_data_frame = pd.concat(all_data_frame)
        return all_data_frame.reset_index(drop=True)

    def __get_data(self, response):
        data_in_string = response.text.split('\n')
        data = []
        for string in data_in_string:
            data.append(string.split('\t'))
        df = pd.DataFrame(data[1:-1], columns=data[0])
        return df
