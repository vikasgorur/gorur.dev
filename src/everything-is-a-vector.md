---
title: "Everything is a Vector"
jupyter: julia-1.10
format:
    html:
        toc: true
        toc-location: left
        toc-expand: true
        mainfont: "PT Serif"
        code-fold: false
---

There is a simple but powerful idea at the heart of all of Machine Learning. It is considered so obvious that many books and courses treat it as an after-thought. The idea is this:

> All real-world data can be thought of as points in a high-dimensional space.

When you understand this it's like realizing that everything in your computer is stored as bits.

In this post we will explore the power of this idea by applying the same simple ML algorithm to
different kinds of vectors.

## Nearest neighbors

Describe the Wifi dataset: https://archive.ics.uci.edu/dataset/422/wireless+indoor+localization

Signal strength of 7 access points, collected in two rooms.
We will use a simplified version with only `w5` and `w7`.

```{julia}
using CSV, DataFrames, MarkdownTables

wifi = CSV.read(
    "data/wifi.tsv",
    DataFrame,
    header=["w1", "w2", "w3", "w4", "w5", "w6", "w7", "room"]
)
wifi = wifi[(wifi.room .== 1) .| (wifi.room .== 2), [:w5, :w7, :room]]
markdown_table(wifi[rand(1:size(wifi, 1), 5), :])
```

A **vector** in machine learning is a point in $n$-dimensional space.

Distance between two points:

```{julia}
distance(v1, v2) = sqrt(sum((v1 - v2).^2))
distance([0, 0], [3, 4])
```

`sortperm` - return indexes of the form [smallest element, next smallest element, ...]
```{julia}
print(sortperm([4, 3, 1, 2]))
```

Describe the knn algorithm.

- points with labels
- knn

```{julia}

struct Point
    xn::Vector{Float64}
    label::String
end

function knn(X::Array{Point}, v::Vector{Float64}, k::Int)
    ds = [distance(x.xn, v) for x in X]
    return X[sortperm(ds)[1:k]]
end
```

Example of knn working in 2 dimensions

```{julia}
knn([
    Point([0.0, 0.0], "zero"),
    Point([1.0, 1.0], "one"),
    Point([2.0, 2.0], "two"),
    Point([3.0, 3.0], "three"),
    Point([4.0, 4.0], "four"),
    Point([5.0, 5.0], "five")
], [3.0, 3.0], 3)
```

Turn the dataset into `Point`s.

```{julia}
#| output: false
# Iterate across each row of wifi and create a Point for it
X = [
    Point(collect(row[[:w5, :w7]]), string(row[:room]))
    for row in eachrow(wifi)
]
```

- Explain the prediction algorithm.
- Describe train/test split.
- Result of running knn on the wifi dataset.

```{julia}
using MLUtils

X_test, X_train = splitobs(X, at=0.15)
X_train = collect(X_train)
X_test = collect(X_test)

size(X_train)
"Return the element that occurs most frequently in an array"
function majority(items::Vector{T})::T where T
    c = Dict{T, Int}()
    for it in items
        if !haskey(c, it)
            c[it] = 1
        else
            c[it] += 1
        end
    end
    return sort(collect(c), by=x->x[2], rev=true)[1][1]
end

# Compute the accuracy score
total = 0
correct = 0

for p in X_test
    neighbors = knn(X_train, p.xn, 7)
    label = majority([x.label for x in neighbors])
    if label == p.label
        correct += 1
    end
    total += 1
end

println("Accuracy: $(correct / total * 100.0)%")
```

Draw the scatter plot

```{julia}
using PlotlyJS

plot(scatter(
    x = [p.xn[1] for p in X_train],
    y = [p.xn[2] for p in X_train],
    mode = "markers",
))
```

## Words as vectors

Encode a recipe as a vector by doing a one-hot encoding of each of the words
in the recipe.

Use knn to predict the cuisine of a new recipe.

## Words as vectors (better)

Use text embeddings to turn a recipe into a vector.
How to combine vectors for individual words into vector for the whole recipe?

## closing thoughts

what else are vectors?
- images
- sound

## Further reading

Word2vec paper, won the "test of time" award

*Distributed Representations of Words and Phrases and their Compositionality* https://arxiv.org/abs/1310.4546

The illustrated Word2vec https://jalammar.github.io/illustrated-word2vec/