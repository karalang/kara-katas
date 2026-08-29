// Benchmark mirror of bullscore.kara — LeetCode #299, Bulls and Cows.
// Same algorithm: build boards once, then 12 scoring passes over a flat digit
// array. See ../README.md § Benchmarks.

const N_PAIRS: usize = 400_000;
const PASSES: usize = 12;
const WIDTH: usize = 4;
const ALPHABET: usize = 4;

fn lcg(state: i64) -> i64 {
    (state.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7fffffff
}

fn main() {
    let total = N_PAIRS * WIDTH;
    let mut secrets = vec![0i64; total];
    let mut guesses = vec![0i64; total];

    let mut state: i64 = 20299;
    for i in 0..total {
        state = lcg(state);
        secrets[i] = (state / 65536) % ALPHABET as i64;
        state = lcg(state);
        guesses[i] = (state / 65536) % ALPHABET as i64;
    }

    let mut checksum: i64 = 0;
    for _pass in 0..PASSES {
        for p in 0..N_PAIRS {
            let base = p * WIDTH;
            let mut s_left = [0i64; ALPHABET];
            let mut g_left = [0i64; ALPHABET];
            let mut bulls: i64 = 0;
            let mut cows: i64 = 0;

            for k in 0..WIDTH {
                let sd = secrets[base + k];
                let gd = guesses[base + k];
                if sd == gd {
                    bulls += 1;
                } else {
                    s_left[sd as usize] += 1;
                    g_left[gd as usize] += 1;
                }
            }
            for d in 0..ALPHABET {
                cows += if s_left[d] < g_left[d] { s_left[d] } else { g_left[d] };
            }

            checksum = (checksum * 31 + bulls * 7 + cows) % 1_000_000_007;
        }
    }

    println!("pairs {} passes {} checksum {}", N_PAIRS, PASSES, checksum);
}
