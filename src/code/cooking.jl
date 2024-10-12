# %%
import JSONTables
import DataFrames

using Test

# Read json as a DataFrame
RECIPES = read("lib/data/cooking_train.json", String) |> JSONTables.jsontable |> DataFrames.DataFrame
RECIPES.ingredients = [collect(x) for x in RECIPES.ingredients]
# %%

struct Encoder
    vocab::Dict{String, Int}
end

function learn_encoder(items::Array{Array{String}})::Encoder
    vocab = Dict{String, Int}()
    i = 1
    for it in items,
        tokens in it,
        t in split(tokens, " ")
            t = replace(t, r"[^a-zA-Z]" => "")
            if !haskey(vocab, t)
                vocab[t] = i
                i += 1
            end
    end
    return Encoder(vocab)
end

E = learn_encoder(RECIPES.ingredients)
# %%

function encode(E::Encoder, x::Array{String})::Vector{Float16}
    v = zeros(Float16, length(E.vocab))
    for ing in x,
        t in split(ing, " ")
            t = replace(t, r"[^a-zA-Z]" => "")
            if haskey(E.vocab, t)
                v[E.vocab[t]] = 1
            end
    end
    return v
end

# %%

@test sum(encode(E, RECIPES.ingredients[1])) > 0

# %%
distance(x::Vector{Float16}, y::Vector{Float16})::Float16 = sqrt(sum((x - y).^2))

# %%

function kNN(x::Vector{Float16}, X::Array{Vector{Float16}}, k::Int)::Array{Int}
    d = [distance(x, y) for y in X]
    return sortperm(d)[1:k]
end

# %%

@time INGREDIENTS = [encode(E, RECIPES.ingredients[j]) for j in 1:size(RECIPES, 1)]

# %%
function nearest_recipes(i, n)
    x = encode(E, collect(RECIPES.ingredients[i]))
    k = kNN(x, INGREDIENTS, n)
    return RECIPES[k, :]
end

@time nearest_recipes(1, 5)
# %%

# Get the most frequent element in an array of strings
function majority(items::Array{String})
    c = Dict{String, Int}()
    for it in items
        if !haskey(c, it)
            c[it] = 1
        else
            c[it] += 1
        end
    end
    return sort(collect(c), by=x->x[2], rev=true)[1][1]
end

@test majority(["chinese", "italian", "chinese", "indian", "chinese"]) == "chinese"
# %%

using MLUtils



# %%
function test_eval()
    n = 100
    correct = 0
    for i in 1:n
        x = encode(E, RECIPES.ingredients[i])
        neighbors = kNN(x, INGREDIENTS, 6)
        pred = majority(RECIPES.cuisine[neighbors])
        if pred == RECIPES.cuisine[i]
            correct += 1
        end
    end
    return correct / n
end

test_eval()

#%%

TEST_RECIPES = read("lib/data/cooking_test.json", String) |> JSONTables.jsontable |> DataFrames.DataFrame
TEST_RECIPES.ingredients = [collect(x) for x in TEST_RECIPES.ingredients]
