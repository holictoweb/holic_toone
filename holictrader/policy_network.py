import numpy as np
from keras.models import Sequential
from keras.layers import Activation, LSTM, Dense, BatchNormalization
from keras.optimizers import sgd


class PolicyNetwork:
    def __init__(self, input_dim=0, output_dim=0, lr=0.01):
        '''
        
        :param input_dim: 
        :param output_dim: 
        :param lr: 기본학습속도 (learning rat, LR)
        '''

        self.input_dim = input_dim
        # learning rate 학습속도
        self.lr = lr

        # LSTM 신경망
        self.model = Sequential() # 전체 싱경망을 구성하는 클래스

        # LSTM은 정책 신경망의 노드를 구성하는 class
        # dropuot 50% 과적합 회피
        # 3개의 LSTM 층을 256 차원으로 구성
        self.model.add(LSTM(256, input_shape=(1, input_dim),
                            return_sequences=True, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(LSTM(256, return_sequences=True, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(LSTM(256, return_sequences=False, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(Dense(output_dim))
        self.model.add(Activation('sigmoid')) # 기본학습 알고리즘 sigmmid

        # 최적화 알고리즘과 학습속도 결정
        self.model.compile(optimizer=sgd(lr=lr), loss='mse')
        self.prob = None

    def reset(self):
        self.prob = None

    def predict(self, sample):
        '''
        신경망을 통해 확률 계산
        :param sample: 학습데이터 및 에이전트 상태를 포함한 17차원의 입력
        :return:
        '''
        self.prob = self.model.predict(np.array(sample).reshape((1, -1, self.input_dim)))[0]
        return self.prob

    def train_on_batch(self, x, y):
        return self.model.train_on_batch(x, y)

    def save_model(self, model_path):
        if model_path is not None and self.model is not None:
            self.model.save_weights(model_path, overwrite=True)

    def load_model(self, model_path):
        if model_path is not None:
            self.model.load_weights(model_path)