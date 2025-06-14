import requests
import random
from collections import defaultdict
import os
import csv  # CSV 파일 처리를 위한 모듈
from datetime import datetime  # 파일 이름에 날짜를 사용하기 위한 모듈

# 콘솔 화면을 깨끗하게 지우기 위한 함수
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_chzzk_live_streams(limit=100):
    """치지직 API를 호출하여 현재 라이브 중인 스트리머 목록을 가져옵니다."""
    api_url = f"https://api.chzzk.naver.com/service/v1/lives?limit={limit}&sortType=POPULAR"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        live_streams = data.get('content', {}).get('data', [])
        return [s for s in live_streams if s.get('liveCategoryValue')]
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return None

def display_top_streams(limit):
    """지정한 수만큼 인기 라이브 방송 목록을 출력합니다."""
    clear_console()
    print(f"==========================================")
    print(f"| 📺 치지직 인기 라이브 방송 TOP {limit}     |")
    print(f"==========================================")
    
    streams = get_chzzk_live_streams(limit)
    
    if not streams:
        print("\n라이브 방송 정보를 가져오는데 실패했습니다.")
        return

    for i, stream_info in enumerate(streams[:limit]):
        streamer_name = stream_info.get('channel', {}).get('channelName', 'N/A')
        live_title = stream_info.get('liveTitle', 'N/A').strip()
        viewer_count = stream_info.get('concurrentUserCount', 0)
        
        print(f"\n{i+1}. {streamer_name} ({viewer_count:,}명)")
        print(f"   - {live_title}")
    print("\n" + "="*42)

def display_top_categories():
    """인기 카테고리 TOP 10을 집계하여 방송 수와 총 시청자 수를 함께 출력합니다."""
    clear_console()
    print(f"===========================================================")
    print(f"| 📊 치지직 인기 카테고리 TOP 10 (시청자 순)              |")
    print(f"===========================================================")

    streams = get_chzzk_live_streams(100)
    
    if not streams:
        print("\n카테고리 정보를 가져오는데 실패했습니다.")
        return

    category_data = defaultdict(lambda: {'count': 0, 'viewers': 0})

    for stream in streams:
        category = stream.get('liveCategoryValue')
        viewers = stream.get('concurrentUserCount', 0)
        if category:
            category_data[category]['count'] += 1
            category_data[category]['viewers'] += viewers
    
    sorted_categories = sorted(
        category_data.items(), 
        key=lambda item: item[1]['viewers'], 
        reverse=True
    )

    print("\n| 순위 | 카테고리          | 방송 수 | 총 시청자 수     |")
    print("-----------------------------------------------------------")
    for i, (category, data) in enumerate(sorted_categories[:10]):
        count = data['count']
        total_viewers = data['viewers']
        print(f"| {i+1:<4} | {category:<17} | {count:<7} | {total_viewers:>12,d} |")
    print("-----------------------------------------------------------")

def recommend_random_streamer():
    """랜덤한 스트리머 한 명을 추천합니다."""
    clear_console()
    print(f"==========================================")
    print(f"| 🎲 오늘의 랜덤 스트리머 추천!          |")
    print(f"==========================================")

    streams = get_chzzk_live_streams(50)
    
    if not streams:
        print("\n스트리머 정보를 가져오는데 실패했습니다.")
        return

    random_stream = random.choice(streams)
    
    streamer_name = random_stream.get('channel', {}).get('channelName', 'N/A')
    live_title = random_stream.get('liveTitle', 'N/A').strip()
    viewer_count = random_stream.get('concurrentUserCount', 0)
    category = random_stream.get('liveCategoryValue', 'N/A')

    print("\n이 스트리머는 어떠세요?\n")
    print(f"■ 스트리머: {streamer_name}")
    print(f"  - 방송 제목: {live_title}")
    print(f"  - 현재 시청자: {viewer_count:,}명")
    print(f"  - 카테고리: {category}")
    print("\n" + "="*42)


def save_to_csv():
    """인기 라이브 방송 30개 정보를 CSV 파일로 저장합니다."""
    clear_console()
    print(f"==========================================")
    print(f"| 💾 인기 방송 TOP 30 CSV 파일로 저장   |")
    print(f"==========================================")

    streams = get_chzzk_live_streams(100)

    if not streams:
        print("\n데이터를 가져오지 못해 파일 저장에 실패했습니다.")
        return

    # 날짜를 포함한 파일 이름 생성
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"chzzk_live_streams_{date_str}.csv"

    try:
        # 파일을 쓰기 모드로 열기 (한글 깨짐 방지를 위해 encoding='utf-8-sig')
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            # CSV 작성기 생성
            writer = csv.writer(f)
            
            # 1. 헤더(열 제목) 작성
            writer.writerow(['스트리머', '방송 제목', '현재 시청자', '카테고리'])
            
            # 2. 내용 작성
            for stream in streams:
                writer.writerow([
                    stream.get('channel', {}).get('channelName', ''),
                    stream.get('liveTitle', '').strip(),
                    stream.get('concurrentUserCount', 0),
                    stream.get('liveCategoryValue', '')
                ])
        
        print(f"\n✅ 성공! {len(streams)}개의 방송 정보가 '{filename}' 파일에 저장되었습니다.")

    except Exception as e:
        print(f"\n❌ 파일 저장 중 오류가 발생했습니다: {e}")


def main():
    """메인 로직: 메뉴를 보여주고 사용자 입력을 받아 함수를 실행합니다."""
    while True:
        clear_console()
        print("==========================================")
        print("| 1. 치지직 인기 라이브 방송 TOP 30      |")
        print("| 2. 치지직 인기 라이브 방송 TOP 20      |")
        print("| 3. 치지직 인기 라이브 방송 TOP 10      |")
        print("| 4. 치지직 인기 카테고리 TOP 10         |")
        print("| 5. 랜덤 스트리머 추천                  |")
        print("| 6. 파일에 저장(csv)                    |") 
        print("| 0. 프로그램 종료                       |")
        print("==========================================")
        
        choice = input("[원하시는 서비스에 해당하는 번호를 입력하세요.]: ")

        if choice == '1':
            display_top_streams(30)
        elif choice == '2':
            display_top_streams(20)
        elif choice == '3':
            display_top_streams(10)
        elif choice == '4':
            display_top_categories()
        elif choice == '5':
            recommend_random_streamer()
        elif choice == '6':
            save_to_csv() 
        elif choice == '0':
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("\n잘못된 입력입니다. 0-6 사이의 번호를 입력해주세요.")

        input("\n엔터 키를 누르면 메인 메뉴로 돌아갑니다...")

if __name__ == "__main__":
    main()