
import CSV
using DataFrames

using Test

wifi = CSV.read(
    "lib/data/wifi.tsv",
    DataFrame,
    header=["w1", "w2", "w3", "w4", "w5", "w6", "w7", "room"]
)

room1 = wifi[wifi.room .== 1, :]
room2 = wifi[wifi.room .== 2, :]
# get the mean of every column for room1
# turn room1 into an array
# then get the mean of each column

room1_mean = mean(Matrix(room1), dims=1)
println(room1_mean)
room2_mean = mean(Matrix(room2), dims=1)
println(room2_mean)

# %%
# plot w5, w7 for room 1 & 2

using PlotlyJS

trace1 = scatter(x=room1.w5, y=room1.w7, mode="markers", marker_color="red", name="room1")
trace2 = scatter(x=room2.w5, y=room2.w7, mode="markers", marker_color="blue", name="room2")
plot([trace1, trace2], Layout(title="Room 1 & 2"))

