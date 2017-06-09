# coding=utf-8
import keras
import pandas as pd
import time
import matplotlib.pyplot as plt

from stock.lstm_util import lstm


def data_predict(test_data, model):
    seq_len = 50
    # x 指第a天后seq_len天的数据（不包括第a天），y 指第a天数据
    x_test, y_test = lstm.deal_data(test_data, seq_len, True)
    predictions = lstm.predict_point_by_point(model, x_test)
    return predictions, y_test


def build_model(train_data):
    epochs = 1
    seq_len = 50
    # x 指第a天后seq_len天的数据（不包括第a天），y 指第a天数据
    x_train, y_train = lstm.deal_data(train_data, seq_len, True)
    model = lstm.build_model([1, 50, 100, 1])
    model.fit(
        x_train,
        y_train,
        batch_size=128,
        nb_epoch=epochs,
        validation_split=0.05)
    return model
