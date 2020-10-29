from lib.settings import *
from lib.GetCOVID19 import GetCOVID19


covi19_info = GetCOVID19(HOSTNAME, USERNAME, PASSWORD, COVID19API)

# print(covi19_info.sort_by_country_name())

# print(covi19_info.sort_by_total_confirmed())

# print(covi19_info.sort_by_new_confirmed())

covi19_info.menu()
