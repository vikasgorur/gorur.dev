# %%
module Phonecalls
function hello()
    println("Hello, world!")
end
function phonecalls()
    # True if there is at least one call per day
    oneperday(days::Vector{Int}) = !any(d -> d == 0, days)

    N = 100000
    days = zeros(Int, 7)
    count = 0
    for _ in 1:N
        for _ in 1:12
            days[rand(1:7)] += 1
        end
        if oneperday(days)
            count += 1
        end
        fill!(days, 0)
    end
    count / N
end

@time phonecalls()

# 0.228355

# %%

# how?
a1 = binomial(12, 7) * factorial(7) * binomial(12, 5) / 7^12

# %%
solution = 3162075840 / 7^12

# %%
# A universe in which dice aren't all "fair"

using Distributions

struct Die
    sides::Vector{Float64}
end

function Die()
    # Create a vector of 6 elements, each a normal variable with mean 1/6 and variance 1/36
    sides = [rand(Normal(1/6, 1/36)) for _ in 1:6]
    sides /= sum(sides)
    Die(sides)
end

Die()
end
