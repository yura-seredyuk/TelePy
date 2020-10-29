from lib.settings import *
from lib.GetCOVID19 import GetCOVID19


covi19_info = GetCOVID19(HOSTNAME, USERNAME, PASSWORD, COVID19API)

# print(covi19_info.sort_by_country_name())

# print(covi19_info.sort_by_total_confirmed())

# print(covi19_info.sort_by_new_confirmed())

covi19_info.menu()

# l = [11, 22, 33, 44, 55]
# template = "|{0:^9}|{1:^10}|{2:^15}|{3:^7}|{4:^10}|"
# print(template.format("CLASSID", "DEPT", "COURSE NUMBER", "AREA", "TITLE"))  # header
# template = "|{0:9}|{1:>10}|{2:>15}|{3:>7}|{4:>10}|"
# print(template.format(*l))
