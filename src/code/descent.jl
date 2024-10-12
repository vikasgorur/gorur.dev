# %%
import CSV
using DataFrames, MarkdownTables

metrics = CSV.read("src/data/metrics.csv", DataFrame)

Rn = Vector{Float64}

scale(V) = (V .- minimum(V)) ./ (maximum(V) - minimum(V))

X::Rn = scale(metrics[!, :n])
Y::Rn = scale(metrics[!, :duration])

# %%

prediction(x::Float64, θ::Rn) = θ[1] .+ θ[2] * x
prediction(X::Rn, θ::Rn) = θ[1] .+ θ[2] * X

#loss(X::Rn, Y::Rn, θ::Rn) = sum((Y .- (θ[1] .+ θ[2] .* X)).^2)
loss(X::Rn, Y::Rn, θ::Rn) = sum((Y - prediction(X, θ)).^2)

function batch_gradient(X::Rn, Y::Rn, θ::Rn, _::Int)
    δ = zeros(2)
    for i in eachindex(X)
        δ[1] += 2 * (prediction(X[i], θ) - Y[i])
        δ[2] += 2 * (prediction(X[i], θ) - Y[i]) * X[i]
    end
    δ
end

# %%
function stochastic_gradient(X::Rn, Y::Rn, θ::Rn, i::Int)
    δ = zeros(2)
    i = i % length(X) + 1
    δ[1] += 2 * (prediction(X[i], θ) - Y[i])
    δ[2] += 2 * (prediction(X[i], θ) - Y[i]) * X[i]
    δ
end

# %%

Trace = Tuple{Vector{Int}, Vector{Float64}}

function descend(gradient, λ)::Tuple{Rn, Trace}
    θ = [-1.0, 1.0]    # Initial values of params
    iters = []
    losses::Rn = []

    l = loss(X, Y, θ)
    for i in 1:100000
        prev_loss = l
        l = loss(X, Y, θ)

        # Bail out if the loss has converged
        if i > 1 && abs(prev_loss - l) < 1e-6
            break
        end

        # Record progress
        if i == 1 || i % 100 == 0
            push!(iters, i)
            push!(losses, l)
        end

        # Compute gradient and update params
        δ = gradient(X, Y, θ, i)
        θ = θ .- λ .* δ
    end
    θ, (iters, losses)
end

# %%

θ_batch, trace_batch = descend(batch_gradient, 1e-4)
θ_stochastic, trace_stochastic = descend(stochastic_gradient, 2e-2)

# %%
for (i, l) in zip(trace[1], trace[2])
    print("iter = $i, loss = $l\n")
end

print(θ)

# %%
using PlotlyJS

# Plot X and Y points
p1 = scatter(x=X, y=Y, mode="markers", name="Data")

# Plot the regression line
x = range(0, stop=1, length=100)
y_batch = θ_batch[1] .+ θ_batch[2] .* x
y_stochastic = θ_stochastic[1] .+ θ_stochastic[2] .* x
p2 = scatter(x=x, y=y_batch, mode="lines", name="Model (batch)")
p3 = scatter(x=x, y=y_stochastic, mode="lines", name="Model (stochastic)")

plot([p1, p2, p3])

# %%

# Plot the loss curve
p4 = scatter(x=trace_batch[1], y=trace_batch[2], mode="lines", name="Loss (batch)")
p5 = scatter(x=trace_stochastic[1], y=trace_stochastic[2], mode="markers", name="Loss (stochastic)")
plot([p4, p5])