from keras.models import Sequential
from keras.layers import LSTM, SimpleRNN, Dense
from sklearn.svm import SVC
import numpy as np
import pandas as pd


"""
模型函數設計區
"""


class StockML:
    def __init__(self) -> None:
        pass

    def time_steps_pre_process(self, df, time_steps):
        if type(df) == pd.DataFrame:
            feature_num = df.iloc[:, :-1].shape[1]
            X = []
            Y = []
            for i in range(len(df) - time_steps+1):
                X.append(df.iloc[i:i+time_steps, :-1].values)
                Y.append(df.iloc[i+time_steps-1, -1])
        elif type(df) == pd.Series:
            feature_num = df.iloc[:-1].shape[0]
            X = [df.iloc[:-1].values.astype('float32')]
            Y = [df.iloc[-1]]
        X = np.array(X)
        Y = np.array(Y)
        X = X.reshape(X.shape[0], time_steps, feature_num)
        return X, Y, feature_num

    def lstm_model(self, df, time_steps=1):
        X_train, y_train, features = self.time_steps_pre_process(df, time_steps)
        model = Sequential()
        model.add(LSTM(64, input_shape=(time_steps, features), return_sequences=True))
        model.add(LSTM(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=15, batch_size=16,)
        return model


    def lstm_predict(self, model, df, time_steps=1):
        X_test, y_test, input_dim = self.time_steps_pre_process(df, time_steps)
        predict = list(model.predict(X_test).reshape(-1))
        return predict[0] if len(predict)==1 else predict


    def rnn_model(self, df, time_steps=1):
        X_train, y_train, features = self.time_steps_pre_process(df, time_steps)
        model = Sequential()
        model.add(SimpleRNN(50, activation='relu', input_shape=(time_steps, features)))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy')
        model.fit(X_train, y_train, epochs=10, batch_size=32)
        return model
    

    def rnn_predict(self, model, df, time_steps=1):
        X_test, y_test, input_dim = self.time_steps_pre_process(df, time_steps)
        predict = list(model.predict(X_test).reshape(-1))
        print(len(predict))
        return predict[0] if len(predict)==1 else predict
    

    def svc_model(self, df, C=1.0):
        X_train = df.iloc[:, :-1]
        y_train = df.iloc[:, -1]
        svm_classifier = SVC(kernel='sigmoid')
        svm_classifier.fit(X_train, y_train)
        return svm_classifier
    

    def svc_predict(self, model, df):
        # df 放測試範圍的資料
        X_test = df.iloc[:, :-1]
        return model.predict(X_test)
