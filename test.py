from CNN_utils import *
from model import *

data_dir = './test/ex_test'
X_ex_test, y_ex_test = make_ex_data(data_dir)

model_dict = {
    'CNN1': CNN1(),
    'CNN2' : CNN2(),
    'CNN3' : CNN3()
}

for model_name, model in model_dict.items() :
    evaluate_model(model, model_name, X_ex_test, y_ex_test)

generator = tf.keras.models.load_model(f'./model_save/GAN/gen_full.h5')
discriminator = tf.keras.models.load_model(f'./model_save/GAN/disc_full.h5')

cal_metrics(generator, discriminator, X_ex_test, y_ex_test)
model_name = 'GAN'
save_img(generator, model_name, X_ex_test, y_ex_test, './test/pred/')

num = 5

for num in range(num):
    sal_list = []
    sal1 = make_sal(X_test[num],  CNN1_model)
    sal2 = make_sal(X_test[num],  CNN2_model)
    sal3 = make_sal(X_test[num],  CNN3_model)
    sal4 = make_sal(X_test[num],  generator)

    sal_list = [sal1, sal2, sal3, sal4]

    save_sal(X_test[num], sal_list, num, './test/sal/')
