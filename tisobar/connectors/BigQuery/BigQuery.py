from google.cloud import bigquery


class BigQuery:
    def __init__(self, path_to_json):
        self.client = bigquery.Client.from_service_account_json(path_to_json)
        self.project = self.client.project
        self.data_sets = [data_set.dataset_id for data_set in list(self.client.list_datasets())]
        self.tables_in_data_set = self.get_tables()

    def get_tables(self):
        tables = {}
        for data_set_id in self.data_sets:
            data_set_ref = self.client.dataset(data_set_id)
            tables_list = list(self.client.list_tables(data_set_ref))
            tables[data_set_id] = [table.table_id for table in tables_list]
        return tables

    def create_schema(self, schema_dict):
        schema = []
        for key, value in schema_dict.items():
            schema.append(bigquery.SchemaField(key, value))
        return schema

    def create_data_set(self, data_set_id):
        data_set_ref = self.client.dataset(data_set_id)
        data_set = bigquery.Dataset(data_set_ref)
        self.client.create_dataset(data_set)

    def delete_data_set(self, data_set_id, delete_contents=False):
        data_set_ref = self.client.dataset(data_set_id)
        self.client.delete_dataset(data_set_ref, delete_contents)

    def create_table(self, data_set_id, table_id, schema_dict):
        data_set_ref = self.client.dataset(data_set_id)
        schema = self.create_schema(schema_dict)
        table_ref = data_set_ref.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        self.client.create_table(table)

    def insert_rows(self, data_set_id, table_id, list_of_tuples):
        table_ref = self.client.dataset(data_set_id).table(table_id)
        table = self.client.get_table(table_ref)
        slice_data = self.slice(list_of_tuples, limit=3000, slice_list=[])
        #TODO: Проверка на размер данных и автоматический подбор нужного  limit
        for one_slice in slice_data:
            self.client.insert_rows(table, one_slice)

    def get_table_schema(self, data_set_id, table_id):
        data_set_ref = self.client.dataset(data_set_id)
        table_ref = data_set_ref.table(table_id)
        table = self.client.get_table(table_ref)
        return table.schema

    def slice(self, slice_data, limit=100, slice_list=[]):
        count = len(slice_data)
        if count > limit:
            slice_list.append(slice_data[:limit])
            return self.slice(slice_data[limit:], limit, slice_list=slice_list)
        else:
            slice_list.append(slice_data)
            return slice_list
        return slice_list

    def get_table_num_rows(self, data_set_id, table_id):
        data_set_ref = self.client.dataset(data_set_id)
        table_ref = data_set_ref.table(table_id)
        table = self.client.get_table(table_ref)
        return table.num_rows

    def get_query(self, sql):
        query_job = self.client.query(sql, location='US')
        result = []
        for row in query_job:
            result.append(list(row))
        return result
