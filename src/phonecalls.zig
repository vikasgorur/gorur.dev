const std = @import("std");

var pcg = std.Random.Pcg.init(0xca24a8e91f6e4c8f);
const rand = pcg.random();

pub fn main() !void {
    const tic = std.time.microTimestamp();
    var week = [7]u8{ 0, 0, 0, 0, 0, 0, 0 };
    const N = 1_000_000;

    var count: u32 = 0;

    for (0..N) |_| {
        @memset(&week, 0);

        var idx: usize = 0;
        for (0..12) |_| {
            idx = rand.intRangeAtMost(u8, 0, 6);
            week[idx] += 1;
        }

        for (week) |d| {
            if (d == 0) {
                count += 1;
                break;
            }
        }
    }

    const p: f64 = (N - @as(f64, @floatFromInt(count))) / N;
    const toc = std.time.microTimestamp();
    const duration: f64 = @as(f64, @floatFromInt(toc - tic)) / 1000.0;
    std.debug.print("{d}, {d}ms\n", .{ p, duration });
}
