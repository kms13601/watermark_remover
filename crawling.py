import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException
from PIL import Image
import urllib.request

chrome_options = webdriver.ChromeOptions()

def create_save_directory(query):
    save_dir = f"./crawling_data/{query}"
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def image_urls(query, image_count):
    # 구글 이미지 페이지 로드
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/imghp")

    # 검색어 입력
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(query)
    search_bar.submit()

    # 페이지 로딩 대기
    time.sleep(2)

    # 이미지 URL 수집
    urls = set()  # 중복 방지를 위해 set 사용
    img_elements = driver.find_elements(By.CSS_SELECTOR, ".F0uyec")  
    for i, img_element in enumerate(img_elements):
        if len(urls) >= image_count:  # 지정한 개수만큼 수집
            break

        try:
            # 썸네일 이미지 클릭
            driver.execute_script("arguments[0].click();", img_element)
            time.sleep(2)  # 로딩 대기

            try:
                large_img_element = driver.find_element(
                    By.XPATH,
                    '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]',
                )
                img_src = large_img_element.get_attribute("src")
                if img_src and img_src.startswith("http") and not img_src.lower().endswith(".gif"):
                    urls.add(img_src)  # set에 추가하여 중복 방지
            except Exception:
                continue

        except (StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"이미지 로드 중 예외 발생: {e}")
            continue

    driver.close()
    return list(urls)

def download_webp_image(url):
    save_path = 'temp_image.webp'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"이미지 다운로드 완료: {save_path}")
    except Exception as e:
        print(f"이미지 다운로드 실패: {e}")

def convert_webp_to_png(output_path):
    webp_path = 'temp_image.webp'
    try:
        with Image.open(webp_path) as img:
            img = img.convert("RGB")  # PNG는 RGB 모드로 저장
            img.save(output_path, "PNG")
        print(f"변환 완료: {output_path}")
    except Exception as e:
        print(f"변환 실패: {e}")

def download_images(query, urls, save_dir):
    for i, url in enumerate(urls):
        try:
            # 파일 확장자 추출
            ext = url.split('.')[-1]
            if ext in ['jpg', 'jpeg', 'png']:
                file_path = os.path.join(save_dir, f"{query}_{i + 1}.{ext}")
                urllib.request.urlretrieve(url, file_path)
                print(f"이미지 저장 완료: {file_path}")
            elif ext == 'webp':
                download_webp_image(url)
                convert_webp_to_png(os.path.join(save_dir, f"{query}_{i + 1}.png"))

                # 임시 파일 삭제
                if os.path.exists('temp_image.webp'):
                    os.remove('temp_image.webp')
        except Exception as e:
            print(f"이미지 저장 실패: {e}")

if __name__ == "__main__":
    # 검색어와 이미지 수 입력
    query = input("검색어를 입력하세요: ").strip()
    image_count = int(input("다운로드할 이미지 개수를 입력하세요: ").strip())

    # 저장 디렉토리 생성
    save_dir = create_save_directory(query)

    # 이미지 URL 수집
    urls = image_urls(query, image_count)
    print(f"{len(urls)}개의 이미지를 찾았습니다.")

    # 이미지 다운로드
    download_images(query, urls, save_dir)
    print(f"{query}의 이미지 다운로드가 완료되었습니다.")
