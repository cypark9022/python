import requests
from bs4 import BeautifulSoup
import datetime

# 오늘 날짜와 현재 시간을 변수에 저장 (가장 최근의 데이터를 확인하기 위해)
now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')
nowHour = now.strftime('%H')

# 브라우저를 통한 접속으로 보이기위해 헤더변수 설정, 순위를 매길 rank 변수 초기값 설정
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
rank = 1

# 오늘날짜, 현재시간의 URL 주소(지니뮤직)로 html 가져오기
# Top200 까지 전부 가져오기위해 1~4까지 반복 (페이지마다 50개씩)
for i in range(1, 5):
    url = 'https://www.genie.co.kr/chart/top200?ditc=D&ymd=' + nowDate + '&hh=' + nowHour + '&rtm=Y&pg=' + str(i)
    data = requests.get(url, headers=headers)

    # beautifulsoup 으로 파싱하여 음원차트(50개) data 가져오기
    soup = BeautifulSoup(data.text, 'html.parser')
    musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr > td.info')

    # musics (tr들) 의 반복문 돌리기
    for music in musics:
        # music 에 있는 a 태그들을 클래스명으로 파싱하여 저장
        title = music.select_one('a.title')
        artist = music.select_one('a.artist')
        album = music.select_one('a.albumtitle')

        # 앞뒤 공백을 제거한 text 값을 변수에 저장
        title = title.text.strip()
        artist = artist.text.strip()
        album = album.text.strip()

        # title 에 19금 아이콘이 있을 경우, 중간공백 제거 후 ()로 표현
        if '19금' in title:
            title = title.replace('19금', '', 1)
            title = title.strip()
            title = '(19금)' + title

        # 출력 후 rank 1씩 증가
        print(rank, title, artist, album, sep='\t|\t')
        rank += 1
