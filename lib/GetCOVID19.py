import mysql.connector
import requests
if __name__ == "__main__":
    pass


class GetCOVID19:
    def __init__(self, HOSTNAME, USERNAME, PASSWORD, COVID19API):
        self.__COVID19API = COVID19API
        self.__db = mysql.connector.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSWORD
        )
        # self.__template = "{0:8}|{1:10}|{2:15}|{3:7}|{4:10}"
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS telepy")
        self.__cursor.execute("USE telepy")
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS Countries (id INT AUTO_INCREMENT PRIMARY KEY, Country VARCHAR(64), CountryCode VARCHAR(3), Slug VARCHAR(128), NewConfirmed INT, TotalConfirmed INT, NewDeaths INT, TotalDeaths INT, NewRecovered INT, TotalRecovered INT, Date VARCHAR(128))")
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS Global (NewConfirmed INT, TotalConfirmed INT, NewDeaths INT, TotalDeaths INT, NewRecovered INT, TotalRecovered INT)")
        # self.__add_info()
        self.__get_covid19_info()

    def __get_covid19_info(self):
        # print("Inside")
        responce = requests.get(self.__COVID19API)
        covid_data = responce.json()
        # print("API => ", covid_data)
        self.__cursor.execute("TRUNCATE Countries")
        for item in covid_data['Countries']:
            sql = "INSERT INTO Countries (Country, CountryCode, Slug, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered, Date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (item['Country'], item['CountryCode'], item['Slug'], item['NewConfirmed'], item['TotalConfirmed'],
                   item['NewDeaths'], item['TotalDeaths'], item['NewRecovered'], item['TotalRecovered'], item['Date'])
            self.__cursor.execute(sql, val)
        self.__db.commit()
        self.__cursor.execute("TRUNCATE Global")
        item = covid_data['Global']
        sql = "INSERT INTO Global (NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (item['NewConfirmed'], item['TotalConfirmed'], item['NewDeaths'],
               item['TotalDeaths'], item['NewRecovered'], item['TotalRecovered'])
        self.__cursor.execute(sql, val)
        self.__db.commit()

    def menu(self):
        exit = False
        while not exit:
            choice = int(input(
                "1. Sort by total confirmed\n2. Sort by new confirmed\n3. Sort by country name\n4. Global information\n0 Exit\n ===>> "))
            if choice == 1:
                self.sort_by_total_confirmed()
            elif choice == 2:
                self.sort_by_new_confirmed()
            elif choice == 3:
                self.sort_by_country_name()
            elif choice == 4:
                self.show_global_info()
            elif choice == 0:
                exit = True
                print("Bye!")
            else:
                print("Wrong choice.")

    def sort_by_total_confirmed(self):
        self.__cursor.execute(
            "SELECT Country, TotalConfirmed FROM Countries ORDER BY TotalConfirmed")
        # for item in self.__cursor.fetchall():
        #     print(' '.join(map(str, item)))
        print("Information sort by total confirmed".center(50, '_'))
        template = "|{0:_^31}|{1:_^16}|"
        print(template.format(*[d[0]
                                for d in self.__cursor.description]))
        template = "|{0:_<31}|{1:_^16}|"
        for item in self.__cursor.fetchall():
            print(template.format(*item))

    def sort_by_new_confirmed(self):
        self.__cursor.execute(
            "SELECT Country, NewConfirmed FROM Countries ORDER BY NewConfirmed")
        # for item in self.__cursor.fetchall():
        #     print(' '.join(map(str, item)))
        print("Information sort by new confirmed".center(48, '_'))
        template = "|{0:_^31}|{1:_^14}|"
        print(template.format(*[d[0]
                                for d in self.__cursor.description]))
        template = "|{0:_<31}|{1:_^14}|"
        for item in self.__cursor.fetchall():
            print(template.format(*item))

    def sort_by_country_name(self):
        self.__cursor.execute(
            "SELECT Country, CountryCode, Slug, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered, Date FROM Countries ORDER BY Country")
        print("Information sort by country name".center(179, '_'))
        template = "|{0:_^31}|{1:_^11}|{2:_^32}|{3:_^12}|{4:_^14}|{5:_^9}|{6:_^11}|{7:_^12}|{8:_^14}|{9:_^22}|"
        print(template.format(*[d[0]
                                for d in self.__cursor.description]))
        template = "|{0:_<31}|{1:_^11}|{2:_<32}|{3:_^12}|{4:_^14}|{5:_^9}|{6:_^11}|{7:_^12}|{8:_^14}|{9:_^22}|"
        for item in self.__cursor.fetchall():
            print(template.format(*item))

    def show_global_info(self):
        self.__cursor.execute(
            "SELECT NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered FROM Global")
        print("Global information".center(93, '_'))
        # [print("  ", d[0], ": ", i, sep="") for d, i in zip(
        #     self.__cursor.description, self.__cursor.fetchone())]
        template = "|{0:^16}|{1:^16}|{2:^11}|{3:^13}|{4:^14}|{5:^16}|"
        print(template.format(*[d[0]
                                for d in self.__cursor.description]))
        print(template.format(*self.__cursor.fetchone()))
