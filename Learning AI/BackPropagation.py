#! /usr/bin/python3


import math
import random
import functools
import operator


class NeuralNetwork(object):
	def __init__(self, input_layer_size, output_layer_size,  hidden_layer_size_list = None, learning_rate = 0.5, *args):
		# Hidden layers.
		if not hidden_layer_size_list:
			hidden_layer_size_list = [math.ceil((input_layer_size + output_layer_size) / 2)]

		hidden_layers = [NeuronLayer(layer_size=hidden_layer_size_list[0], prev_layer_size=input_layer_size)]

		if len(hidden_layer_size_list) > 1:
			prev_size = hidden_layer_size_list[0]

			for size in hidden_layer_size_list[1:]:
				hidden_layers.append(NeuronLayer(layer_size=size, prev_layer_size=prev_size))
				prev_size = size

		self.hidden_layers = hidden_layers

		# Output layer.
		self.output_layer = OutputNeuronLayer(layer_size=output_layer_size, prev_layer_size=hidden_layer_size_list[-1])

		# Other attributes.
		self.learning_rate = learning_rate


	def feed_forward(self, input_values):
		for layer in self.hidden_layers:
			layer.feed_forward(input_values)
			input_values = layer.get_output_values()

		self.output_layer.feed_forward(input_values)


	def propagate_backward(self, input_values, target_output_values):
		# Update deltas of layers.
		self.output_layer.calc_delta_values(target_output_values)

		next_layer_neurons = self.output_layer.neurons

		for idx in range(len(self.hidden_layers)-1, -1, -1):
			prev_layer_output_values = input_values if idx == 0 else self.hidden_layers[idx-1].get_output_values()

			current_hidden_layer = self.hidden_layers[idx]
			current_hidden_layer.calc_delta_values(next_layer_neurons)
			next_layer_neurons = current_hidden_layer.neurons

		# Update weights
		self.output_layer.update_weights(self.hidden_layers[-1].get_output_values(), self.learning_rate)

		for idx in range(len(self.hidden_layers)-1, -1, -1):
			prev_layer_output_values = input_values if idx == 0 else self.hidden_layers[idx-1].get_output_values()

			current_hidden_layer = self.hidden_layers[idx]
			current_hidden_layer.update_weights(prev_layer_output_values, self.learning_rate)


	def train(self, input_values, target_output_values):
		self.feed_forward(input_values)
		print("ERROR:", self.output_layer.get_total_error(target_output_values))
		self.propagate_backward(input_values, target_output_values)


	def input_to_output(self, input_values):
		self.feed_forward(input_values)
		return self.output_layer.get_output_values()


class Neuron(object):
	def __init__(self, weight_count):
		k = 1 / math.sqrt(weight_count)
		self.weights = [random.uniform(-k, k) for _ in range(weight_count)]
		self.bias_value = 0.01
		self.out = float()			# To store activation value
		self.delta = float()


	def logistic_func(self, tot_net_inp):
		return 1 / (1 + math.exp(-tot_net_inp))


	def calc_output_value(self, prev_layer_output_values):
		tot_net_inp = 0

		for out, weight in zip(prev_layer_output_values , self.weights):
			tot_net_inp += out * weight

		tot_net_inp += self.bias_value

		self.out = self.logistic_func(tot_net_inp)


class NeuronLayer(object):
	def __init__(self, layer_size, prev_layer_size, *args):
		self.neurons = [Neuron(prev_layer_size) for _ in range(layer_size)]


	def feed_forward(self, prev_layer_output_values):
		for neuron in self.neurons:
			neuron.calc_output_value(prev_layer_output_values)


	def get_output_values(self, *args):
		return [neuron.out for neuron in self.neurons]


	def calc_delta_values(self, next_layer_neurons):
		for idx, neuron in enumerate(self.neurons):
			s = functools.reduce(operator.add, [neu.weights[idx] * neu.delta for neu in next_layer_neurons], 0)
			neuron.delta = s * neuron.out * (1 - neuron.out)


	def update_weights(self, prev_layer_output_values, learning_rate):
		for neuron in self.neurons:
			for idx, out in enumerate(prev_layer_output_values):
				neuron.weights[idx] -= learning_rate * out * neuron.delta
				neuron.bias_value -= learning_rate * neuron.delta


class OutputNeuronLayer(NeuronLayer):
	def __init__(self, **kwargs):
		super(OutputNeuronLayer, self).__init__(**kwargs)
		# self.neurons is inherited.


	def calc_delta_values(self, target_output_values):		# Over-written method.
		for neuron, target in zip(self.neurons, target_output_values):
			out = neuron.out
			neuron.delta = -(target - out) * out * (1 - out)


	def get_total_error(self, target_output_values):
		tot_error = 0

		for t, o in zip(target_output_values, self.get_output_values()):
			tot_error += 0.5 * (t - o) * (t - o)

		return tot_error


def main():
	nn = NeuralNetwork(3, 3, [5], 0.5)

	training_set = [
		[[0, 0, 0], [0, 0, 1]],
		[[0, 0, 1], [0, 1, 0]],
		[[0, 1, 0], [0, 1, 1]],
		[[0, 1, 1], [1, 0, 0]],
		[[1, 0, 0], [1, 0, 1]],
		[[1, 0, 1], [1, 1, 0]],
		[[1, 1, 0], [1, 1, 1]],
		[[1, 1, 1], [0, 0, 0]]]

	# Training.
	for i in range(10000):
		for inp, out in training_set:
			nn.train(inp, out)

	# Exam.
	for inp, out in training_set:
		L = [round(x) for x in nn.input_to_output(inp)]
		print(L, L == out)


if __name__ == '__main__':
	main()