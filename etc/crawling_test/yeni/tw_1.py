from requests_html import HTMLSession
import re                               #re라는 정규표현식 모듈을 불러와서 사용

session = HTMLSession()         #웹 페이지에 접속하기 위해 준비. (일을 시키기 위한 일꾼 준비)
r = session.get('https://twitter.com/boannews') #해당 웹페이지에 접속하여 그 결과를 r 변수에 저장
#'보안뉴스'트위터에서 보안뉴스 기사 url이 담긴 부분의 경로
extract_news_link = 'body > #doc > #page-outer > #page-container > div > div > div > div > div > div > #timeline > div > div > #stream-items-id > .js-stream-item.stream-item.stream-item > div > div.content > div.js-tweet-text-container > p > a'

#트위터에서 긁어온 보안뉴스 기사 url을 저장할 list형 변수 news_url 선언
news_url = list()

f1 = open("twitter_html.txt", "w", encoding='UTF-8')
f2 = open("twitter_tag.txt", "w", encoding='UTF-8')

#render(): 자바스크립트가 실행된 html 코드를 받아올수 있게 하는 함수
#트위터는 스크롤을 내리면 계속해서 밑에 내용이 추가되는 형태로 이루어짐
#코드로 스크롤을 n번 시킴. 스크롤해서 바로 뜨는게 아니라 200ms를 쉬고 나온 html 결과를 가져옴.
r.html.render(scrolldown=1,sleep=0.2)


def news_crawl(r2):
    
    raw_data = r2.text          #보안뉴스 기사의 html
    print(raw_data)
    #f1.write(raw_data)
    

    
    url = r2.url                 #보안뉴스 기사의 url
    f2.write('url: ')
    f2.write(url)
    f2.write('\n')
    print('url: ',url)
    

    #제목, 날짜, 내용, 작성자 별로 크롤링 하여 변수 저장 및 출력
    
    for line2 in r2.html.find('div#news_title02'):
        news_title = line2.text
        f2.write('제목: ')
        f2.write(news_title)
        f2.write('\n')
        print('제목: ', news_title)

    for line2 in r2.html.find('div#news_util01'):
        date = line2.text
        f2.write('날짜: ')
        f2.write(date[8:])
        f2.write('\n')
        print('날짜: ', date[8:])

    for line2 in r2.html.find('div#news_content'):
        writer = re.search(r'\[[가-힣\s]*\]',line2.text)
        if(writer!=None):
                f2.write('작성자: ')
                f2.write(writer.group())
                f2.write('\n')
                print('작성자: ', writer.group())

    origin = '보안뉴스'
    f2.write('출처: ')
    f2.write(origin)
    f2.write('\n')
    
    for line2 in r2.html.find('div#news_content'):
        content = re.sub(r'\[[가-힣\s]*[=][\sa-zA-Z0-9]*\]', '', line2.text )
        print('내용: ', content)
        f2.write('내용: ')
        f2.write(content)
        f2.write('\n')

    for line2 in r.html.find('div#news_tag_txt'):
        tag = line2.text
        f2.write('태그')
        f2.write(tag)
        f2.write('\n')
        print('태그: ', tag)

    f2.write("\n")
    
        
    print('\n')

    
#r.이라는 객체가 얻어온 html 코드를 얻어와서 find()를 사용하여 경로를 지정해줘서 해당 경로에 위치하는 태그 객체를 얻어온다 
#line.links로 얻을 수 있는 보안뉴스 기사 url의 단축url은 크롤링이 안되는 오류가 생겨서
#line.text로 긴 url을 얻어옴. 해당 url의 경우 'https://www.boannews.com/media/view.asp?idx=83776 …' 형태로 크롤링이 되므로
#…을 제거하고 공백을 제거하여 리스트 형 변수 news_url에 넣어줌 
for line in r.html.find(extract_news_link):
    url = line.text.replace('…','')         #...제거
    url_len = len(url)
    news_url.append(url[:url_len-1])            #공백제거
    
    

#news_url에 저장된 트위터에서 읽어온 뉴스url을 r2변수에 저장 및 함수로 보내기
for url in news_url:
    r2 = session.get(url)
    news_crawl(r2)
    #print(url)


f1.close()
f2.close()
    
 
