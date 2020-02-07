import requests
import time


class VKApp:
    def __init__(self, access_token, account_id, client_id):
        self.__access_token = access_token
        self.__v = "5.101"
        self.__method_url = "https://api.vk.com/method/"
        self.account_id = account_id
        self.client_id = client_id

    def get_profile_info(self):
        profile_info = self.__request('users.get', request_type='get')[0]
        return profile_info['first_name'], profile_info['last_name'], profile_info['id']

    def __slice(self, slice_ids, limit=100, slice_list=[]):
        count = len(slice_ids)
        if count > limit:
            slice_list.append(slice_ids[:limit])
            return self.__slice(slice_ids[limit:], limit, slice_list=slice_list)
        else:
            slice_list.append(slice_ids)
            return slice_list
        return slice_list

    def __request(self, method, request_type='get', **kwargs):
        if "access_token" not in kwargs:
            params = {'access_token': self.__access_token, 'v': self.__v}
            for key, value in kwargs.items():
                params[key] = value
        else:
            params = kwargs
        request_data = requests.request(request_type, self.__method_url + method, params=params).json()
        return self.get_errors(request_data, method, params, request_type, i=0)

    def get_errors(self, response, method, params, request_type, i=0):
        if "error" in response:
            time.sleep(7)
            if (response['error']['error_code'] not in [100, 9]) or (i > 5):
                raise Exception(response['error'])
            else:
                data = self.__request(method, request_type, **params)
                i += 1
                return self.get_errors(data, method, params, request_type, i=i)
        elif 'response' in response:
            return response['response']
        else:
            raise Exception("Это что-то новое")

    def get_accounts(self):
        accounts = self.__request('ads.getAccounts', request_type='get')
        return accounts

    def get_clients(self, accounts):
        all_clients = []
        for account_id in accounts:
            clients = self.__request('ads.getClients', request_type='get', account_id=account_id)
            for client in clients:
                client['account_id'] = account_id
                all_clients.append(client)
            time.sleep(2)
        return all_clients

    def get_campaigns(self):
        campaigns = self.__request('ads.getCampaigns', request_type='get', account_id=self.account_id,
                                   include_deleted=1, client_id=self.client_id)
        return campaigns

    def get_ads(self, campaign_ids):
        campaign_ids = self.__slice(campaign_ids, slice_list=[])
        ads_list = []
        for campaign_ids_list in campaign_ids:
            campaign_ids_string = ",".join([str(x) for x in campaign_ids_list])
            ads = self.__request('ads.getAds', request_type='get', account_id=self.account_id,
                                 campaign_ids=f"[{campaign_ids_string}]", client_id=self.client_id)
            for ad in ads:
                ads_list.append(ad)
            time.sleep(2)
        return ads_list

    def get_groups(self):
        groups = self.__request('groups.get', request_type='get', extended=1)
        return groups['items']

    def get_day_stats(self, ids_type, list_of_ids, date_from, date_to, limit=2000):
        day_stat_list = []
        ids_list = self.__slice(list_of_ids, limit, slice_list=[])
        for ids_stat_list in ids_list:
            ids_stat_string = ",".join([str(x) for x in ids_stat_list])
            day_stats = self.__request('ads.getStatistics', request_type='get', account_id=self.account_id,
                                       ids_type=ids_type, ids=ids_stat_string, period="day", date_from=date_from,
                                       date_to=date_to)
            for DayStat in day_stats:
                for stat in DayStat['stats']:
                    day_stat_list.append(stat)
            time.sleep(2)
        return day_stat_list

    def get_posts_reach(self, post_reach_list_ids, limit=100):
        posts_reach = []
        post_reach_list = self.__slice(post_reach_list_ids, limit, slice_list=[])
        for PostReach_id_list in post_reach_list:
            post_reach_ids_string = ",".join([str(x) for x in PostReach_id_list])
            post_reach_response = self.__request('ads.getPostsReach', request_type='get', account_id=self.account_id,
                                                 ids_type="ad", ids=post_reach_ids_string)
            for PostReach_stat in post_reach_response:
                posts_reach.append(PostReach_stat)
            time.sleep(2)
        return posts_reach

    # TODO: Доделать лбработку результатов в get_demographics
    def get_demographics(self, demographics_list_ids, date_from, date_to, limit=2000):
        demographics = []
        demographics_list = self.__slice(demographics_list_ids, limit, slice_list=[])
        for Demographics_id_list in demographics_list:
            demographics_ids_string = ",".join([str(x) for x in Demographics_id_list])
            demographics_response = self.__request('ads.getDemographics', request_type='get',
                                                   account_id=self.account_id, ids_type="ad",
                                                   ids=demographics_ids_string, period="day",
                                                   date_from=date_from, date_to=date_to)
            demographics.append(demographics_response)
        return demographics

    def get_ads_layout(self, ads_list_ids, limit=2000):
        ads_layout = []
        ads_layout_list = self.__slice(ads_list_ids, limit, slice_list=[])
        for AdsLayout_id_list in ads_layout_list:
            ads_layout_ids_string = ",".join([str(x) for x in AdsLayout_id_list])
            ads_layout_response = self.__request('ads.getAdsLayout', request_type='get', account_id=self.account_id,
                                                 client_id=self.client_id, ad_ids=f"[{ads_layout_ids_string}]",
                                                 include_deleted=1)
            for AdsLayout_stat in ads_layout_response:
                ads_layout.append(AdsLayout_stat)
            time.sleep(2)
        return ads_layout
