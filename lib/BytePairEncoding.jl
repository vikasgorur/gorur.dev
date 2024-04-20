
# %%

# Print the codepoints of the string
print([Int(x) for x in "hi 😀"])

# %%

# Get the UTF-8 bytes of the string

transcode(UInt8, "hi 😀")

HOLMES = collect(transcode(UInt8, read("holmes.txt", String)[1:16384]))

# %%

# Find the most common pair of tokens
function mostcommonpair(tokens)
    pairs = Dict{Tuple{UInt8, UInt8}, Int}()
    for i in 1:length(tokens)-1
        pair = (tokens[i], tokens[i+1])
        pairs[pair] = get(pairs, pair, 0) + 1
    end
    return argmax(pairs)
end

print("Most common pair: `$(transcode(String, collect(mostcommonpair(TOKENS))))`")

# %%
# Replace the most common pair with a new token

function replacepair!(tokens, pair, newtoken)
    i = 1
    while i < length(tokens)
        if tokens[i] == pair[1] && tokens[i+1] == pair[2]
            tokens[i] = newtoken
            splice!(tokens, i+1)
        end
        i += 1
    end
end

function merged(tokens::Vector{UInt8}, n::Int)::Tuple{Vector{UInt8}, Dict{UInt16, Vector{UInt8}}}
    result = copy(tokens)
    vocab = Dict{UInt16, Vector{UInt8}}()
    newtoken = 256
    for i in 1:n
        pair = mostcommonpair(result)
        vocab[newtoken] = collect(pair)
        print("Merging $(pair) into $(newtoken)\n")
        replacepair!(result, pair, newtoken)
        newtoken += 1
    end
    return result, vocab
end

# %%

using Printf

print("tokens length: $(length(HOLMES))\n")
ids, vocab = merged(HOLMES, 25)
print("merged length: $(length(ids))\n")
@printf "compression ratio: %.2f" length(HOLMES)/length(ids)

# %%

function decode(tokens::Vector{UInt8}, vocab::Dict{UInt8, Vector{UInt8}})::String
    for i in 0:255
        vocab[i] = [i]
    end
    result = ""
    for token in tokens
        result *= transcode(String, vocab[token])
    end
    return result
end

# %%
decode(ids[1:1024], vocab)