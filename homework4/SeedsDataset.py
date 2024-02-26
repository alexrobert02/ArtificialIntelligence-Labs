import numpy as np


def data_split(data, test_size=0.2, random_seed=None):
    if random_seed is not None:
        np.random.seed(random_seed)

    data = np.array(data)
    test_size = int(len(data) * test_size)

    indices = np.arange(len(data))
    np.random.shuffle(indices)

    test_indices = indices[:test_size]
    train_indices = indices[test_size:]

    test_set = data[test_indices]
    train_set = data[train_indices]

    # Extrage input-urile (x) și output-urile (y)
    x_train, y_train = train_set[:, :-1], train_set[:, -1]  # Features de antrenare, Clase de antrenare
    x_test, y_test = test_set[:, :-1], test_set[:, -1]  # Features de testare, Clase de testare

    return x_train, x_test, y_train, y_test


def read_and_split_data(file_path):
    # Citirea datelor din fișier
    data = np.loadtxt(file_path)

    # Împărțirea setului de date în antrenare și testare (80% antrenare, 20% testare)
    x_train, x_test, y_train, y_test = data_split(data, test_size=0.2, random_seed=42)
    print(f"x_train: {x_train.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"x_test: {x_test.shape}")
    print(f"y_test: {y_test.shape}")

    return x_train, x_test, y_train, y_test


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return sigmoid(z) * (1 - sigmoid(z))


class SeedsDataset:
    def __init__(self, file_path):
        self.x_train, self.x_test, self.y_train, self.y_test = read_and_split_data(file_path)
        self.y_train = self.y_train - 1
        self.y_test = self.y_test - 1
        self.parameters = self.initialize_parameters()

    def initialize_parameters(self):
        # Inițializarea parametrilor și ponderilor
        input_size = self.x_train.shape[1]
        hidden_size1 = 5
        hidden_size2 = 3
        output_size = 3
        learning_rate = 0.01
        max_epochs = 1000

        np.random.seed(42)
        w1 = np.random.randn(input_size, hidden_size1)
        b1 = np.zeros((1, hidden_size1))
        w2 = np.random.randn(hidden_size1, hidden_size2)
        b2 = np.zeros((1, hidden_size2))
        w3 = np.random.randn(hidden_size2, output_size)
        b3 = np.zeros((1, output_size))

        parameters = {
            "input_size": input_size,
            "hidden_size1": hidden_size1,
            "hidden_size2": hidden_size2,
            "output_size": output_size,
            "learning_rate": learning_rate,
            "max_epochs": max_epochs,
            "w1": w1,
            "b1": b1,
            "w2": w2,
            "b2": b2,
            "w3": w3,
            "b3": b3
        }
        return parameters

    def mean_squared_error(self, y, y_hat):
        y_reshape = np.eye(3)[y.astype(int)]
        return 1 / (2 * len(self.x_train)) * np.power(y_reshape - y_hat, 2)

    def forward_propagation(self, x):
        # Extragem parametrii
        w1 = self.parameters["w1"]
        b1 = self.parameters["b1"]
        w2 = self.parameters["w2"]
        b2 = self.parameters["b2"]
        w3 = self.parameters["w3"]
        b3 = self.parameters["b3"]

        # Propagarea înainte
        z1 = np.dot(x, w1) + b1
        a1 = sigmoid(z1)
        z2 = np.dot(a1, w2) + b2
        a2 = sigmoid(z2)
        z3 = np.dot(a2, w3) + b3
        y_hat = sigmoid(z3)

        cache = {
            "z1": z1,
            "a1": a1,
            "z2": z2,
            "a2": a2,
            "z3": z3,
            "y_hat": y_hat
        }

        return y_hat, cache

    def backward_propagation(self, x, y, cache):
        # Extragem parametrii
        w1 = self.parameters["w1"]
        w2 = self.parameters["w2"]
        w3 = self.parameters["w3"]

        # Extragem cache-ul
        z1 = cache["z1"]
        a1 = cache["a1"]
        z2 = cache["z2"]
        a2 = cache["a2"]
        z3 = cache["z3"]
        y_hat = cache["y_hat"]

        # Propagarea înapoi
        y_reshape = np.eye(3)[y.astype(int)]
        dz3 = y_hat - y_reshape
        dw3 = 1 / x.shape[0] * np.dot(a2.T, dz3)
        db3 = 1 / x.shape[0] * np.sum(dz3, axis=0, keepdims=True)

        dz2 = np.dot(dz3, w3.T) * sigmoid_derivative(z2)
        dw2 = 1 / x.shape[0] * np.dot(a1.T, dz2)
        db2 = 1 / x.shape[0] * np.sum(dz2, axis=0, keepdims=True)

        dz1 = np.dot(dz2, w2.T) * sigmoid_derivative(z1)
        dw1 = 1 / x.shape[0] * np.dot(x.T, dz1)
        db1 = 1 / x.shape[0] * np.sum(dz1, axis=0, keepdims=True)

        gradients = {
            "dw3": dw3,
            "db3": db3,
            "dw2": dw2,
            "db2": db2,
            "dw1": dw1,
            "db1": db1
        }

        return gradients

    def update_parameters(self, gradients):
        learning_rate = self.parameters["learning_rate"]

        self.parameters["w1"] = self.parameters["w1"] - learning_rate * gradients["dw1"]
        self.parameters["b1"] = self.parameters["b1"] - learning_rate * gradients["db1"]
        self.parameters["w2"] = self.parameters["w2"] - learning_rate * gradients["dw2"]
        self.parameters["b2"] = self.parameters["b2"] - learning_rate * gradients["db2"]
        self.parameters["w3"] = self.parameters["w3"] - learning_rate * gradients["dw3"]
        self.parameters["b3"] = self.parameters["b3"] - learning_rate * gradients["db3"]

        return self.parameters

    def train(self):
        x_train = self.x_train
        y_train = self.y_train
        max_epochs = self.parameters["max_epochs"]

        for epoch in range(max_epochs):
            # Propagarea înainte
            y_hat, cache = self.forward_propagation(x_train)

            # Calcularea funcției de cost
            cost = self.mean_squared_error(y_train, y_hat)

            # Propagarea înapoi
            gradients = self.backward_propagation(x_train, y_train, cache)

            # Actualizarea parametrilor
            self.parameters = self.update_parameters(gradients)

            if epoch % 100 == 0:
                print(f"Cost after epoch {epoch}: {cost}")

        return self.parameters

    def evaluate_accuracy(self, x, y):
        y_hat, _ = self.forward_propagation(x)
        y_hat = np.argmax(y_hat, axis=1)
        correct_predictions = np.sum(y_hat == y)
        accuracy = correct_predictions / y.shape[0]

        print(f"Number of correct predictions: {correct_predictions} out of {y.shape[0]}")
        return accuracy

    def confusion_matrix(self, x, y):
        y_hat, _ = self.forward_propagation(x)
        y_hat = np.argmax(y_hat, axis=1)
        y = y-1
        y = y.astype(int)
        y_hat = y_hat.astype(int)
        cm = np.zeros((3, 3))
        for i in range(y.shape[0]):
            cm[y[i], y_hat[i]] += 1
        return cm

    def precision(self, x, y):
        cm = self.confusion_matrix(x, y)
        sum_per_class = np.sum(cm, axis=0)
        precision_values = np.zeros_like(sum_per_class, dtype=float)
        for i in range(len(sum_per_class)):
            if sum_per_class[i] != 0:
                precision_values[i] = cm[i, i] / sum_per_class[i]
            else:
                precision_values[i] = 0  # sau o valoare predefinită relevantă
        return precision_values

    def recall(self, x, y):
        cm = self.confusion_matrix(x, y)
        return np.diag(cm) / np.sum(cm, axis=1)

    def f1_score(self, x, y):
        prec = self.precision(x, y)
        rec = self.recall(x, y)
        f1 = np.zeros_like(prec, dtype=float)
        for i in range(len(prec)):
            if prec[i] + rec[i] != 0:
                f1[i] = 2 * prec[i] * rec[i] / (prec[i] + rec[i])
            else:
                f1[i] = 0  # sau o valoare predefinită relevantă
        return f1
