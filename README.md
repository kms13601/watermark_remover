0️⃣ **간단한 데이터 셋이 포함되어 있습니다. 3️⃣으로 건너뛰어도 무방합니다**

##

1️⃣ **이미지 크롤링**
```
python crawling.py
```
⚠️ 검색어가 한글일 경우 이미지 이름이 한글로 저장되어, 이미지 파일 read가 힘듭니다. 가급적 영어 사용해주세요

![result](/MD/crawling.gif) 

##

2️⃣ **이미지에 로고 합성**

```
cd overlay
python overlay.py
```

모델을 처음부터 훈련시키려면 data 폴더 내부의 data, data1, data2, data3, data4 폴더를 모두 삭제하세요

그리고 crawling_data 폴더를 ./data/로 옮긴 후, data로 이름을 변경하세요

생성된 data1~data4 폴더를 ./data/로 옮기세요

```
ㄴdata
  ㄴdata(crawling_data를 rename한 것)
  ㄴdata1
  ㄴdata2
  ㄴdata3
  ㄴdata4
```

이렇게 만들면 됩니다.

overlay.py의 line 21-22는 외부 검증 데이터를 위한 코드입니다. 외부 검증 데이터가 필요하다면 각주를 해제하고 코드를 실행하세요. 각주를 해제한다면 data5와 data6 이라는 폴더가 생성됩다

이때 다음과 같은 과정이 필요합니다
1. crawling.py에서 외부 검증 데이터가 저장되는 디렉토리를 변경해주기(line 13)
2. ./overlay/overlay.py 에서 외부 검증 데이터가 저장된 path로 변경해주기(line 5)
3. ./test/ 에 있는 모든 폴더 삭제하기
4. 1에서 디렉토리 이름을 external_crawl 로 설정했다면, external_crawl 폴더를 ./test/로 옮긴 후, ex_test로 폴더명 변경
5. data5, data6 폴더를 ./test/로 옮긴 후, ex_test1, ex_test2로 이름 변경해주기

##

3️⃣ **모델 훈련**


사용된 버전은 다음과 같습니다. 
```
python = 3.9.19
keras = 2.14.0
numPy = 1.26.4
```

```
python CNN.py
python GAN.py

--- 이후의 과정은 선택입니다 ---
python saliency_map.py
python test.py
```

## 
4️⃣ **결과**

![result](/MD/result.png) 
![sal](/MD/sal.png)   


이미지1(결과)
이미지2(sal)

##
5️⃣ **참고**

GAN: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git의 코드를 변형하여 사용
