import requests

class Calltouch:
    def __init__(self, ct_site_id, ct_token):
        self.__ct_token = ct_token
        self.__url = f'http://api.calltouch.ru/calls-service/RestAPI/{ct_site_id}/calls-diary/calls'

    def __get_pages(self, date_from, date_to):
        params = {'clientApiId': self.__ct_token, 'dateFrom': date_from, 'dateTo': date_to, 'page': 1, 'limit': 1000}
        response = requests.get(self.__url, params=params).json()['pageTotal']
        return response

    def get_calls(self, date_from, date_to):
        i = 1
        total_result = []
        pages = self.__get_pages(date_from, date_to)
        keys = ['callId', 'callerNumber', 'date', 'waitingConnect', 'duration', 'phoneNumber', 'successful',
                'uniqueCall', 'targetCall', 'uniqTargetCall', 'callbackCall', 'city', 'source', 'medium', 'keyword',
                'callUrl', 'utmSource', 'utmMedium', 'utmCampaign', 'utmContent', 'utmTerm', 'sessionId', 'ctCallerId',
                'clientId', 'yaClientId', 'sipCallId', 'callTags', 'callUrl']

        while i <= pages:
            params = {'clientApiId': self.__ct_token, 'dateFrom': date_from, 'dateTo': date_to, 'page': i,
                      'limit': 1000, 'withCallTags': True}
            list_of_calls = requests.get(self.__url, params=params).json()['records']
            i += 1
            for call in list_of_calls:
                data = call.copy()
                for key, values in call.items():
                    if key not in keys:
                        data.pop(key)
                    elif key == 'callTags':
                        for one in values:
                            if (one['type'] == 'AUTO-PR') or (one['type'] == 'MANUAL'):
                                data[one['type']] = ",".join(one['names'])
                        data.pop("callTags")
                total_result.append(data)
        return total_result
