from model import predict
from db import init_fb
import os

def calc_percentage(block_list):
    return int((len([a for a in block_list if a == 'Ripe']) / len(block_list)) * 100)

def init_predict():
    input_pth = "iot_input"
    list_block_pth = os.listdir(input_pth)

    total_prediction = []
    temp_result ={}
    for l_pth in list_block_pth:
        predictions = []
        list_img = os.listdir(input_pth + '/' + l_pth)
        for i in list_img:
            img_pth = input_pth + '/' + l_pth + '/' + i
            predictions.append(predict(img_pth)[0])
        temp_result['accuracy'] = calc_percentage(predictions)
        temp_result['predictions'] = predictions
        total_prediction.append(temp_result.copy())

    return(total_prediction)


db = init_fb()
ref = db.reference("/Grading")

update_data = init_predict()

for i, data in enumerate(update_data):
    ref.child(str(chr(65 + i))).set(data)
