// Bench mirror of maxsub_bench.kara — Kadane over a batch of LCG-generated arrays,
// i64 sink of per-array answers. rustc -O. See ../README.md § Benchmarks.

fn main() {
    let m: i64 = 1103515245; // glibc LCG multiplier
    let inc: i64 = 12345; // glibc LCG increment
    let modulus: i64 = 2147483648; // 2^31
    let windows: i64 = 120000; // number of simulated input arrays
    let w: i64 = 1000; // length of each array

    let mut state: i64 = 1; // LCG seed
    let mut sink: i64 = 0;
    let mut k: i64 = 0;
    while k < windows {
        state = (state * m + inc) % modulus;
        let v0 = (state % 100) - 50;
        let mut best = v0;
        let mut here = v0;
        let mut j = 1i64;
        while j < w {
            state = (state * m + inc) % modulus;
            let v = (state % 100) - 50;
            here = if here + v > v { here + v } else { v };
            if here > best {
                best = here;
            }
            j += 1;
        }
        sink += best;
        k += 1;
    }
    println!("{}", sink);
}
