% This script is to find number of clusters in data set.
% Data is supplied in a file named 'data.txt'

% Number of clusters.
k = 3;

% Load data
X = load('data.txt');
m = size(X, 1);
n = size(X, 2);

% Randomly shuffle the rows of X.
X = X( randperm(m), :);

% Plot data
plot(X(:, 1), X(:, 2), 'k+','LineWidth', 2, 'MarkerSize', 7);
hold on;

%  Initialize centroids.
X1_min = min(X(:, 1));
X1_max = max(X(:, 1));

X2_min = min(X(:, 2));
X2_max = max(X(:, 2));

centroids = zeros(k, n);
centroids_final = zeros(k, n);
J_final = intmax( 'int64' );

for iter = 1: 1000
    for i = 1:k
        centroids(i, :) = X(randi(m), :);
    end

    % Plot centroids.
    % plot(centroids(:, 1), centroids(:, 2), 'r+','LineWidth', 2, 'MarkerSize', 7);
    % hold off;
    % fprintf("Press enter to continue\n");
    % pause;
    % close;

    % Loop over

    prev_J = intmax('int64');
    curr_J = prev_J - 1;

    while prev_J > curr_J
        prev_J = curr_J;
        curr_J = 0;
        
        c = zeros(m, 1);
        
        for i = 1:m
            [val, idx] = min(sum((X(i, :) - centroids) .^ 2, 2));
            c(i) = idx;
            curr_J += val;
        end

        for i = 1:k
            idx = find(c == i);
            
            if ~isempty(idx)    
                centroids(i, :) = mean(X(idx, :));
            endif
        end
    end
    
    if J_final > curr_J
        J_final = curr_J
        centroids_final = centroids;
    end
end

% Plot data and centroids.
close;
plot(centroids_final(:, 1), centroids_final(:, 2), 'r+','LineWidth', 2, 'MarkerSize', 7);
hold on;

markerColors = {'g+', 'b+', 'y+', 'm+', 'c+'};

for i = 1:k
    idx = find(c == i);
    plot(X(idx, 1), X(idx, 2), markerColors{i},'LineWidth', 2, 'MarkerSize', 7);
    hold on;
endfor

hold off;