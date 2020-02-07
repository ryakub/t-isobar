def record_to_tuple(list_of_records):
    result_list = []
    for record in list_of_records:
        result_list.append(tuple(list(record)[1:]))
    return result_list


def convert_types(result_list, int_list, float_list):
    data = []
    for record in result_list:
        record_list = list(record)
        data_list = []
        for key, value in enumerate(record_list):
            if key in int_list:
                data_list.append(int(value))
            elif key in float_list:
                data_list.append(float(value))
            else:
                data_list.append(str(value))
        data_list = tuple(data_list)
        data.append(data_list)
    return data


def total_function(list_of_records, int_list, float_list=[]):
    result_list = record_to_tuple(list_of_records)
    data = convert_types(result_list, int_list, float_list)
    return data
