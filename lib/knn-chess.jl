
import CSV
using DataFrames

using Test

games = CSV.read("lib/data/20k_chess.csv.gz", DataFrame)
games.minutes = (t -> parse(Int, split(t, "+")[1])).(games.increment_code)
println(names(games))

rapid = games[games.minutes .>= 10, :]


# Add a new column "resigned" which is true if victory_status == resign
rapid.draw = rapid.victory_status .== "draw"
rapid.rating_gap = abs.(rapid.white_rating - rapid.black_rating)


using PlotlyJS

# plot draw=true as red, draw=false as blue
trace1 = scatter(x=rapid.rating_gap[rapid.draw], y=rapid.turns[rapid.draw], mode="markers", marker_color="red", name="draw")
trace2 = scatter(x=rapid.rating_gap[.!rapid.draw], y=rapid.turns[.!rapid.draw], mode="markers", marker_color="yellow", name="no draw")
plot([trace1], Layout(title="Draw"))

