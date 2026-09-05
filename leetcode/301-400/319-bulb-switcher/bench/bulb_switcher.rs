// Benchmark mirror of LeetCode #319 — the round simulation.
//
// Same algorithm as bench/bulb_switcher.kara: PASSES passes, each simulating
// n rounds over an n-bulb byte array and folding the count of lit bulbs
// together with the sum of their indices.

const BULBS: i64 = 6000000;
const PASSES: i64 = 10;
const STRIDE: i64 = 90011;
const MASKMOD: i64 = 1073741823;

fn main() {
    let mut on = vec![0u8; (BULBS + 1) as usize];

    let mut sink: i64 = 0;
    for p in 0..PASSES {
        let n = BULBS - p * STRIDE;

        for b in 0..=n as usize {
            on[b] = 0;
        }

        let mut step: i64 = 1;
        while step <= n {
            let mut b = step;
            while b <= n {
                on[b as usize] ^= 1;
                b += step;
            }
            step += 1;
        }

        let mut count: i64 = 0;
        let mut idx_sum: i64 = 0;
        for b in 1..=n {
            if on[b as usize] == 1 {
                count += 1;
                idx_sum = (idx_sum + b) % MASKMOD;
            }
        }
        sink = (sink * 31 + count * 7919 + idx_sum) % MASKMOD;
    }

    println!("checksum {}", sink);
}
