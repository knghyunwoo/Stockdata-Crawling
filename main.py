import requests
import re
from bs4 import BeautifulSoup

# 기업에 대한 정보를 크롤링하는 함수입니다.
def crawling(soup):
    
    name_list, data_list, nowprice_list, before_compare_list, plusminus_list, stock_list = [], [], [], [], [], []
    data_dict = {}
    
    table = soup.find("table", class_="type_5")
    
    names = table.find_all("div", class_="name_area") # 이름 받아오는 부분
    for name in names:
        name_list.append(name.text.replace("\t","").replace("*","").replace("\n",""))
        
    datas = table.find_all("td",class_="number") # 현재가부터 전일거래량까지 모든 숫자를 받아오는 부분
    for data in datas:
        data_list.append(data.text.replace("\t","").replace("*","").replace("\n",""))
    
    for i in range(len(data_list)):
        if i % 8 == 0:
            nowprice_list.append(data_list[i]) # 받아온 부분중 현재가만 저장
        elif i % 8 == 1:
            before_compare_list.append(data_list[i]) # 받아온 부분중 전일비만 저장
        elif i % 8 == 2:
            plusminus_list.append(data_list[i]) # 받아온 부분중 등락률만 저장
    
    for i in range(len(name_list)): # stock 리스트 만드는 부분
        stock_list.append([name_list[i], nowprice_list[i], before_compare_list[i], plusminus_list[i]])
    
    for i in range(len(name_list)): # data 딕셔너리 만드는 부분
        if plusminus_list[i][0] == "+": # 등락률이 + 인것만 찾아서
            data_dict[name_list[i]] = int(nowprice_list[i].replace(",","")) # 현재가를 정수로 바꾸어 data_dict에 넣어줌
    
    data_dict = sorted(data_dict.items(), key=lambda x:x[1]) # 현재가를 오름차순으로 변경
    
    return stock_list, data_dict


def main() :
    # 주어진 url을 크롤링하세요.
    custom_header = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    url = "https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=235"
    req = requests.get(url, headers=custom_header)
    if req.status_code == requests.codes.ok:    
        print("접속 성공")
    
    soup = BeautifulSoup(req.text, "html.parser")
    
    stock, data = crawling(soup)
    print(stock)
    
    # 현재가가 오름차순이 되도록 data 딕셔너리를 출력하세요.
    print(data)

if __name__ == "__main__" :
    main()
