import requests
from bs4 import BeautifulSoup
class Weather():
    @staticmethod
    def get_temperature():
        r = requests.get("http://www.pogodynka.pl/polska/16dni/krakow_krakow")
        soup = BeautifulSoup(r.text, 'html.parser')
        result_list = soup.find_all("tr")
        return (str(result_list[2]).splitlines()[-3][4:-5])