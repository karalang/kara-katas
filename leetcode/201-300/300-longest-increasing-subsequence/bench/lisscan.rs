// Benchmark mirror of lisscan.kara — LeetCode #300, Longest Increasing
// Subsequence. Same patience sorting, same hand-written binary search, same
// reused stack tails buffer. See ../README.md § Benchmarks.

const N_ARRAYS: usize = 3000;
const LEN: usize = 512;
const PASSES: usize = 24;
const SPREAD: i64 = 4096;

fn lcg(state: i64) -> i64 {
    (state.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7fffffff
}

fn main() {
    let total = N_ARRAYS * LEN;
    let mut data = vec![0i64; total];

    let mut state: i64 = 20300;
    for i in 0..total {
        state = lcg(state);
        data[i] = (state / 65536) % SPREAD;
    }

    let mut tails = [0i64; LEN];
    let mut checksum: i64 = 0;

    for _pass in 0..PASSES {
        for a in 0..N_ARRAYS {
            let base = a * LEN;
            let mut n_tails: usize = 0;

            for k in 0..LEN {
                let x = data[base + k];

                let mut lo = 0usize;
                let mut hi = n_tails;
                while lo < hi {
                    let mid = lo + (hi - lo) / 2;
                    if tails[mid] < x { lo = mid + 1; } else { hi = mid; }
                }

                if lo == n_tails {
                    tails[n_tails] = x;
                    n_tails += 1;
                } else {
                    tails[lo] = x;
                }
            }

            checksum = (checksum * 31 + n_tails as i64) % 1_000_000_007;
        }
    }

    println!("arrays {} len {} passes {} checksum {}", N_ARRAYS, LEN, PASSES, checksum);
}
