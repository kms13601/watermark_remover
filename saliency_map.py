from CNN_utils import *
from model import *
from sklearn.model_selection import train_test_split

data_dir = './data'
X, y = make_data(data_dir)

X_train, test_water, y_train, test_non_water = train_test_split(
    X, y, test_size=0.4, random_state=42)

X_val, X_test, y_val, y_test = train_test_split(
    test_water, test_non_water, test_size=0.5, random_state=42)

CNN1_model = load_model(f'./model_save/CNN1', custom_objects={'psnr': psnr, 'ssim': ssim, 'combined_loss': combined_loss})
CNN2_model = load_model(f'./model_save/CNN2', custom_objects={'psnr': psnr, 'ssim': ssim, 'combined_loss': combined_loss})
CNN3_model = load_model(f'./model_save/CNN3', custom_objects={'psnr': psnr, 'ssim': ssim, 'combined_loss': combined_loss})
GAN = tf.keras.models.load_model(f'./model_save/GAN/gen_full.h5')

num = 5

for num in range(num):
    sal_list = []
    sal1 = make_sal(X_test[num],  CNN1_model)
    sal2 = make_sal(X_test[num],  CNN2_model)
    sal3 = make_sal(X_test[num],  CNN3_model)
    sal4 = make_sal(X_test[num],  GAN)

    sal_list = [sal1, sal2, sal3, sal4]

    save_sal(X_test[num], sal_list, num)
