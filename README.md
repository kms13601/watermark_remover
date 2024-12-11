0️⃣ **간단한 데이터 셋이 포함되어 있습니다. 3️⃣으로 건너뛰어도 무방합니다**

##

1️⃣ **이미지 크롤링**
```
python crawling.py
```
⚠️ 검색어가 한글일 경우 이미지 이름이 한글로 저장되어, 이미지 파일 read가 힘듭니다. 가급적 영어 사용해주세요

![crawling](/MD/crawling.gif) 

##

2️⃣ **이미지에 워터마크 합성**

```
cd overlay
python overlay.py
```

1. 모델을 처음부터 훈련시키려면 `data` 폴더 내부의 `data, data1, data2, data3, data4` 폴더를 모두 삭제하세요
2. 그리고 `crawling_data` 폴더를 `./data/`로 옮긴 후, data로 이름을 변경하세요
3. 생성된 `data1~data4` 폴더를 `./data/`로 옮기세요

```
ㄴdata
  ㄴdata(crawling_data를 rename한 것)
  ㄴdata1
  ㄴdata2
  ㄴdata3
  ㄴdata4
```

이렇게 만들면 됩니다.

`overlay.py`의 line 21-22는 외부 검증 데이터를 위한 코드입니다. 외부 검증 데이터가 필요하다면 각주를 해제하고 코드를 실행하세요. 각주를 해제한다면 data5와 data6 이라는 폴더가 생성됩니다

이때 다음과 같은 과정이 필요합니다
1. `crawling.py`에서 외부 검증 데이터가 저장되는 디렉토리를 변경해주기(line 13)
2. `./overlay/overlay.py` 에서 외부 검증 데이터가 저장된 path로 변경해주기(line 5)
3. `./test/` 에 있는 모든 폴더 삭제하기
4. 1에서 디렉토리 이름을 `external_crawl` 로 설정했다면, `external_crawl` 폴더를 `./test/`로 옮긴 후, `ex_test`로 폴더명 변경
5. `data5, data6` 폴더를 `./test/`로 옮긴 후, `ex_test1, ex_test2`로 이름 변경해주기

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

##
5️⃣ **참고**

GAN: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git)의 코드를 변형하여 사용

##
##

0️⃣ **A simple dataset is included. You may skip directly to step 3️⃣if desired.**

##

1️⃣ **Image Crawling**
```
python crawling.py
```
⚠️ If the search keyword is in Korean, image filenames will also be saved in Korean, which may cause issues when reading the images. Please use English whenever possible.

![crawling](/MD/crawling.gif) 

##

2️⃣ **Watermark Synthesis on Images**

```
cd overlay
python overlay.py
```

1. If you want to train the model from scratch, delete the `data`, `data1`, `data2`, `data3`, and `data4` folders inside the `data` directory.
2. Then, move the `crawling_data` folder to `./data/` and rename it to `data`.
3. Move the newly created `data1`~`data4` folders to `./data/`.


```
ㄴdata
  ㄴdata(crawling_data를 rename한 것)
  ㄴdata1
  ㄴdata2
  ㄴdata3
  ㄴdata4
```

This is the required structure.

Lines 21-22 in `overlay.py` are for external validation data. If external validation data is needed, uncomment these lines and run the code. Uncommenting them will create `data5` and `data6` folders.

In this case, follow these steps:
1. Modify the directory where external validation data is stored in `crawling.py` (line 13).
2. Update the path to the external validation data in `./overlay/overlay.py` (line 5).
3. Delete all folders in `./test/`.
4. If the directory name was set to `external_crawl` in step 1, move the `external_crawl` folder to `./test/` and rename it to `ex_test`.
5. Move `data5` and `data6` folders to `./test/` and rename them to `ex_test1` and `ex_test2`, respectively.


##

3️⃣ **Model Training**


The following versions were used: 
```
python = 3.9.19
keras = 2.14.0
numPy = 1.26.4
```

```
python CNN.py
python GAN.py

--- The following steps are optional ---
python saliency_map.py
python test.py
```

## 
4️⃣ **Results**

![result](/MD/result.png) 
![sal](/MD/sal.png)   

##
5️⃣ **References**

GAN: This project uses a modified version of the code from [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git).
