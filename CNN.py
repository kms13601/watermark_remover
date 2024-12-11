from utils import *
from model import *
from sklearn.model_selection import train_test_split

data_dir = './data'
water_images, non_water_images = make_data(data_dir)

X_train, test_water, y_train, test_non_water = train_test_split(
    water_images, non_water_images, test_size=0.4, random_state=42)

X_val, X_test, y_val, y_test = train_test_split(
    test_water, test_non_water, test_size=0.5, random_state=42)

model_dict = {
    'CNN1': CNN1(),
    'CNN2' : CNN2(),
    'CNN3' : CNN3()
}

for model_name, model in model_dict.items() :
    train_and_evaluate_model(model, model_name, X_train, y_train, X_val, y_val, X_test, y_test)
