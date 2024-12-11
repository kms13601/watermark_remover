import cv2
import numpy as np
import os
import random

def add_logo_randomly(img_path, logo_name):
    file_name = img_path.split("\\")[-1].split('.')[0]
    
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    logo = cv2.imread(f'./watermark/{logo_name}.png', cv2.IMREAD_UNCHANGED)
    
    logo_height, logo_width = logo.shape[:2]
    img_height, img_width = img.shape[:2]
    new_logo_width = img_width // 3  
    new_logo_height = int(new_logo_width * logo_height / logo_width)
    logo = cv2.resize(logo, (new_logo_width, new_logo_height), interpolation=cv2.INTER_AREA)

    positions = [
        (0, 0),  # 왼쪽 위
        (img_width - new_logo_width, 0),  # 오른쪽 위
        (0, img_height - new_logo_height),  # 왼쪽 아래
        (img_width - new_logo_width, img_height - new_logo_height)  # 오른쪽 아래
    ]

    selected_position = random.choice(positions)

    alpha = random.uniform(0.2, 0.4)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
    selected_color = random.choice(colors)

    if logo.shape[2] == 3:  
        b, g, r = cv2.split(logo)
        alpha_channel = np.ones(b.shape, dtype=b.dtype) * 255
        logo = cv2.merge((b, g, r, alpha_channel))
    
    for c, color_value in enumerate(selected_color):
        logo[:, :, c] = color_value

    # 위치에 로고 추가
    x, y = selected_position
    roi = img[y:y+new_logo_height, x:x+new_logo_width]

    # 로고 알파 채널 적용
    logo_bgr = logo[:, :, :3]
    logo_alpha = (logo[:, :, 3] / 255.0) * alpha
    inv_alpha = 1.0 - logo_alpha

    for c in range(3):  # B, G, R 채널
        roi[:, :, c] = (logo_bgr[:, :, c] * logo_alpha + roi[:, :, c] * inv_alpha).astype(np.uint8)

    img[y:y+new_logo_height, x:x+new_logo_width] = roi

    os.makedirs(f'./data{logo_name}', exist_ok=True)
    result_path = f"./data{logo_name}/{file_name}.png"
    cv2.imwrite(result_path, img)
    #print(f"결과가 {result_path}에 저장되었습니다.")
    return result_path


def logo_crop(img_path, logo_name):
    file_name = img_path.split("\\")[-1].split('.')[0]

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    logo = cv2.imread(f'./watermark/{logo_name}.png', cv2.IMREAD_UNCHANGED)

    img_height, img_width = img.shape[:2]
    logo_height, logo_width = logo.shape[:2]
    
    alpha = random.uniform(0.2, 0.4)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
    selected_color = random.choice(colors)
    
    for c in range(3): 
        logo[:, :, c] = selected_color[c]

    crop_x = max(0, (logo_width - img_width) // 2)
    crop_y = max(0, (logo_height - img_height) // 2)
    cropped_logo = logo[crop_y:crop_y + img_height, crop_x:crop_x + img_width]

    cropped_logo_height, cropped_logo_width = cropped_logo.shape[:2]

    offset_x = random.randint(-100, 100)
    offset_y = random.randint(-100, 100)
    start_x = max(0, (img_width - cropped_logo_width) // 2 + offset_x)
    start_y = max(0, (img_height - cropped_logo_height) // 2 + offset_y)

    end_x = start_x + cropped_logo_width
    end_y = start_y + cropped_logo_height

    if end_x > img_width:
        end_x = img_width
        start_x = end_x - cropped_logo_width

    if end_y > img_height:
        end_y = img_height
        start_y = end_y - cropped_logo_height

    if cropped_logo.shape[2] == 3:  
        b, g, r = cv2.split(cropped_logo)
        alpha_channel = np.ones(b.shape, dtype=b.dtype) * 255
        cropped_logo = cv2.merge((b, g, r, alpha_channel))

    logo_bgr = cropped_logo[:, :, :3]
    logo_alpha = (cropped_logo[:, :, 3] / 255.0) * alpha
    inv_alpha = 1.0 - logo_alpha

    roi = img[start_y:end_y, start_x:end_x]

    roi_height, roi_width = roi.shape[:2]
    logo_bgr = logo_bgr[:roi_height, :roi_width]
    logo_alpha = logo_alpha[:roi_height, :roi_width]
    inv_alpha = inv_alpha[:roi_height, :roi_width]

    for c in range(3):
        roi[:, :, c] = (logo_bgr[:, :, c] * logo_alpha + roi[:, :, c] * inv_alpha).astype(np.uint8)

    os.makedirs(f'./data{logo_name}', exist_ok=True)
    result_path = f"./data{logo_name}/{file_name}.png"
    cv2.imwrite(result_path, img)
    #print(f"결과가 {result_path}에 저장되었습니다.")
    return result_path
