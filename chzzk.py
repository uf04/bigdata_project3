import requests
import random
from collections import defaultdict
import os

# 콘솔 화면을 깨끗하게 지우기 위한 함수 (Windows, Mac, Linux 호환)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_chzzk_live_streams(limit=100):
    """
    치지직 API를 호출하여 현재 라이브 중인 스트리머 목록을 가져옵니다.
    :param limit: 한 번에 가져올 방송 수 (기본값: 100)
    :return: 라이브 방송 정보가 담긴 리스트 또는 에러 발생 시 None
    """
    api_url = f"https://api.chzzk.naver.com/service/v1/lives?limit={limit}&sortType=POPULAR"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        live_streams = data.get('content', {}).get('data', [])
        # 카테고리가 없는 24시간 채널 등 필터링
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

# ======================================================================
# 아래 함수가 요청에 따라 수정된 부분입니다.
# ======================================================================
def display_top_categories():
    """인기 카테고리 TOP 10을 집계하여 방송 수와 총 시청자 수를 함께 출력합니다."""
    clear_console()
    print(f"===========================================================")
    print(f"| 📊 치지직 인기 카테고리 TOP 10 (시청자 순)              |")
    print(f"===========================================================")

    streams = get_chzzk_live_streams(100) # 더 많은 데이터를 기반으로 집계
    
    if not streams:
        print("\n카테고리 정보를 가져오는데 실패했습니다.")
        return

    # 각 카테고리별로 방송 수와 시청자 수를 합산
    # defaultdict는 키가 없을 경우 지정된 기본값을 자동으로 생성해줍니다.
    category_data = defaultdict(lambda: {'count': 0, 'viewers': 0})

    for stream in streams:
        category = stream.get('liveCategoryValue')
        viewers = stream.get('concurrentUserCount', 0)
        if category:
            category_data[category]['count'] += 1
            category_data[category]['viewers'] += viewers
    
    # 총 시청자 수를 기준으로 내림차순 정렬
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
        # f-string을 사용하여 깔끔하게 정렬하여 출력
        print(f"| {i+1:<4} | {category:<17} | {count:<7} | {total_viewers:>12,d} |")
    print("-----------------------------------------------------------")

def recommend_random_streamer():
    """랜덤한 스트리머 한 명을 추천합니다."""
    clear_console()
    print(f"==========================================")
    print(f"| 🎲 오늘의 랜덤 스트리머 추천!          |")
    print(f"==========================================")

    streams = get_chzzk_live_streams(50) # 상위 50개 중에서 추천
    
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
        elif choice == '0':
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("\n잘못된 입력입니다. 0-5 사이의 번호를 입력해주세요.")

        input("\n엔터 키를 누르면 메인 메뉴로 돌아갑니다...")

if __name__ == "__main__":
    main()