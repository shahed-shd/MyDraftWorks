% Load trainging data set
X = load('dataX.txt');
y = load('dataY.txt');

X = [ones(size(X, 1), 1), X];
[m, n] = size(X);

% Cost function definition
function [jval, grad] = costFunc(X, y, theta)
	m = size(X, 1);
	lambda = 0.125;		% Regularization parameter.

	h = X * theta;
	jval = (1/(2*m)) * sum((h - y) .^ 2) ...
		+ (lambda/(2*m)) * sumsq(theta(2:end));

	grad = (1/m) * sum((h - y) .* X)';
	grad(2:end) += (lambda / m) * theta(2:end);
end

% Initialize theta
epsilon = 1e-4;
init_theta = rand(n, 1) * 2 * epsilon - epsilon;

% Advanced optimization
options = optimset('GradObj', 'on', 'MaxIter', 100);
[opt_theta, funcVal, exitFlag] = fminunc(@(t)costFunc(X, y, t), init_theta, options);

% Load data to predict
X_test = load('dataXtest.txt');
X_test = [ones(size(X_test, 1), 1), X_test];

% Now predict
y_test = X_test * opt_theta
