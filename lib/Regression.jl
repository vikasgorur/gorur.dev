import CSV
using DataFrames

metrics = CSV.read("metrics.csv", DataFrame)
# %%

X = metrics[!, :n]
Y = metrics[!, :duration]

# Scale the X and Y vectors to the range [0, 1]
X = (X .- minimum(X)) ./ (maximum(X) - minimum(X))
Y = (Y .- minimum(Y)) ./ (maximum(Y) - minimum(Y))

# %%

makeloss(X, Y) = (w0, w1) -> sum((Y .- (w0 .+ w1 .* X)).^2)
L = makeloss(X, Y)

# Forward-mode gradient

function fgrad(f, w0, w1)
    step = 1e-6
    δw0 = (f(w0 + step, w1) - f(w0, w1)) / step
    δw1 = (f(w0, w1 + step) - f(w0, w1)) / step
    (δw0, δw1)
end

w0 = -1
w1 = -1

fgrad(L, w0, w1)

# %% Gradient descent to find the optimal w0 and w1

w0 = -1
w1 = -1
print("Starting at loss: $(L(w0, w1))\n")
# Training loop

λ = 1e-2
for i in 1:10000
    δw0, δw1 = fgrad(L, w0, w1)
    global w0 -= λ * δw0
    global w1 -= λ * δw1
end

print("($w0, $w1)\n")
print("Ending at loss: $(L(w0, w1))\n")



# %%

using Zygote

w0 = -1
w1 = -1
loss = makeloss(X, Y)

print("Starting at loss: $(loss(w0, w1))\n")
# Training loop

λ = 1e-2
for i in 1:1000
    δw0, δw1 = gradient(makeloss(X, Y), w0, w1)
    global w0 -= λ * δw0
    global w1 -= λ * δw1
end


print("($w0, $w1)\n")
print("Ending at loss: $(loss(w0, w1))\n")

#%%

# Compute r-square
Ŷ = w0 .+ w1 .* X
Ȳ = sum(Y) / length(Y)
SST = sum((Y .- Ȳ).^2)
SSR = sum((Y .- Ŷ).^2)
R² = 1 - SSR / SST
print("R² = $R²\n")

print("w0 = $w0, w1 = $w1\n")
#%%
# Plot heatmap of the loss function v/s w0 and w1
using PlotlyJS

w0s = range(-1, 1, length=1000)
w1s = range(-1, 1, length=1000)
losses = [loss(w0, w1) for w0 in w0s, w1 in w1s]

plot(heatmap(
    x=w0s,
    y=w1s,
    z=losses,
    colorscale="Viridis",
    colorbar_title="Loss",
    xaxis_title="w0",
    yaxis_title="w1",
))

#%%
# Plot contour plot of the loss function v/s w0 and w1
using PlotlyJS

w0s = range(-1, 1, length=1000)
w1s = range(-1, 1, length=1000)
losses = [loss(w0, w1) for w0 in w0s, w1 in w1s]

plot(contour(
    x=w0s,
    y=w1s,
    z=losses,
    colorscale="Electric",
    colorbar_title="Loss",
    showlabels=true,
    xaxis_title="w0",
    yaxis_title="w1",
))

#%% Perfect hashing

WORDS = [
    "love",
    "rook",
    "duck",
    "mine"
]

chars(w::String) = [c - 'a' for c in collect(w)]

W2 = hcat([11, 14, 21, 4],
[17, 14, 14, 10],
[3, 20, 2, 10],
[12, 8, 13, 4])
m = rand(Float64, 4, 4)


#%% Polynomial interpolation

using PlotlyJS
using LinearAlgebra

points::Vector{Tuple{Float64,Float64}} = [
    (1, 4),
    (2, 9),
    (3, 45),
    (4, 78),
]

xs = [p[1] for p in points]
ys = [p[2] for p in points]

plot(
    scatter(x=xs, y=ys, mode="markers"),
)

# Co-efficients of the polynomial
px::Vector{Float64} = [1, 1, 1, 1]

# Plot the polynomial in the range [0, 6]
xs = range(0, 6, length=100)

# Evaluate the polynomial at x
pval(px::Vector{Float64}, x::Float64) = px ⋅ (x .^ (0:length(px)-1))

plot(
    scatter(x=xs, y=(x -> pval(px, x)).(xs), mode="lines")
)

function ploss(px::Vector{Float64}, points::Vector{Tuple{Float64, Float64}})
    sum((pval(px, p[1]) - p[2])^2 for p in points)
end

ploss(px, points)

using Zygote

gradient(px -> ploss(px, points), px)

# %%

points::Vector{Tuple{Float64,Float64}} = [
    (1, 1),
    (2, 4),
    (3, 14),
    (4, 9),
]

# Training loop
px::Vector{Float64} = rand(Float64, 4)
print("Starting at loss: $(ploss(px, points))\n")

λ = 1e-6
for i in 1:10000
    δpx = gradient(px -> ploss(px, points), px)[1]
    global px -= λ * δpx
end
print("Ending at loss: $(ploss(px, points))\n")

# %%
# Plot the polynomial in the range [0, 6]
xs = range(0, 5, length=100)

p1 = plot(
    scatter(x=xs, y=(x -> pval(px, x)).(xs), mode="lines")
)

# Add the `points`` to the plot as well
addtraces(p1,
    scatter(x=[p[1] for p in points], y=[p[2] for p in points], mode="markers")
)

# %%

# Compute the Lagrange polynomial that passes through the points
function lagrange(points::Vector{Tuple{Float64, Float64}})
    xs = [p[1] for p in points]
    ys = [p[2] for p in points]
    function L(x::Float64)
        sum(ys[i] * prod((x - xs[j]) / (xs[i] - xs[j]) for j in 1:length(points) if j != i) for i in 1:length(points))
    end
    L
end

L = lagrange(points)

# %% plot the Lagrange polynomial

xs = range(0, 5, length=100)

p2 = plot(
    scatter(x=xs, y=(x -> L(x)).(xs), mode="lines")
)

addtraces(p2,
    scatter(x=[p[1] for p in points], y=[p[2] for p in points], mode="markers")
)
