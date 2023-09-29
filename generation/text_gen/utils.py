import os
from typing import List, Dict

def is_empty_file(path):
    return os.stat(path).st_size == 0


def one_field_to_array(queryset_list, id_field, to_arr_field):
    new_dict = {}
    for elem in queryset_list:
        new_dict.setdefault(elem[id_field], []).append(elem[to_arr_field])

    return new_dict

# def one_field_to_array(queryset_list: List[Dict], id_field: str, to_arr_field: str):
#     new_dict = {}
#     for elem in queryset_list:
#         new_dict.setdefault(elem[id_field], []).append(elem[to_arr_field])
#
#     return new_dict