
function [] = octavetest()
	options = optimset('GradObj', 'on', 'MaxIter', 100);
	initialTheta = zeros(3, 1);
	[optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options)
end

function [jVal, grd] = costFunction(theta)
	jVal = (theta(1) - 31) ^ 2 + (theta(2) - 37) ^ 2 + (theta(3) - 41) ^ 2;
	grd = [2 * (theta(1) - 31); 2 * (theta(2) - 37); 2 * (theta(3) - 41)];
end