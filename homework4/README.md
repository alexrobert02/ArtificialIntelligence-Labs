# Neural networks

### Homework
Consider the following dataset https://archive.ics.uci.edu/dataset/236/seeds (210 examples, 7 attributes, 3 classes) which contains information about different varieties of wheat. Use a multi-layer neural network to classify the data. Implement the Backpropagation algorithm.

**Requirements**:
1. Read the data from the file and split the dataset into train and test sets (randomly).
2. Initialize the parameters (the size of the input, of the hidden and the output layer, the learning rate, the maximum number of epochs, etc.) and the weights.
3. Implement the activation functions, the derivatives and the error function.
4. Forward propagation: compute the output of the neurons from the hidden layers and from the output layer.
5. Backpropagation: compute the gradients and update the weights for the neurons from the output and the hidden layer.
6. Train the network for a number of epochs.
7. Predict on the test data set and print the performance metrics.
