import random
from collections import deque

import numpy as np
import keras
from tqdm.auto import tqdm
from keras import layers


keras.utils.disable_interactive_logging()


class ReplayBuffer:
    def __init__(self, max_size=2000):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch_size = max(len(self.buffer), batch_size)
        return random.sample(self.buffer, batch_size)

    def size(self):
        return len(self.buffer)


class DQNAgent:
    def __init__(
            self,
            jobs,
            learning_rate=0.001,
            gamma=0.95,
            epsilon=0.8,
            epsilon_min=0.01,
            epsilon_decay=0.995,
            replay_buffer_size=100,
            batch_size=5
    ):
        self.state_shape = (len(jobs), )
        self.action_size = len(jobs)
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.replay_buffer = ReplayBuffer(max_size=replay_buffer_size)
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _build_model(self):
        model = keras.Sequential([
            layers.Dense(24, input_shape=self.state_shape, activation='relu'),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            ls = list(filter(lambda x: x[1] == 0, enumerate(state[0])))
            sample = random.choice(ls)
            return sample[0]
        q_values = self.model.predict(state)
        ls = list(filter(lambda x: state[0][x[0]], enumerate(q_values[0])))
        if not ls:
            return np.argmax(q_values[0])
        return max(ls, key=lambda x: x[1])[0]

    def replay(self):
        if self.replay_buffer.size() < self.batch_size:
            return

        minibatch = self.replay_buffer.sample(self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env, episodes=1000):
        for e in tqdm(range(episodes)):
            state = env.reset()
            state = np.reshape(state, [1, *self.state_shape])
            for _ in tqdm(range(50)):
                action = self.act(state)
                next_state, reward, done, _ = env.step(action)
                next_state = np.reshape(next_state, [1, *self.state_shape])
                self.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    self.update_target_model()
                    print(f"Episode {e+1}/{episodes}, Score: {reward}, Epsilon: {self.epsilon:.2}")
                    break
                self.replay()
