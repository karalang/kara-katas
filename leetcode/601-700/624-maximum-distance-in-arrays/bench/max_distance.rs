// LeetCode #624: Maximum Distance in Arrays -- Rust mirror of the Kāra
// bench.
//
// The ★ arm's one pass over the same inputs and rounds.

fn max_distance(arrays: &[Vec<i64>]) -> i64 {
    let mut low = arrays[0][0];
    let mut high = arrays[0][arrays[0].len() - 1];
    let mut best = 0;
    for a in &arrays[1..] {
        let first = a[0];
        let last = a[a.len() - 1];
        best = best.max(last - low).max(high - first);
        low = low.min(first);
        high = high.max(last);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_arrays(count: i64, spread: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut arrays = Vec::new();
    for _ in 0..count {
        let mut values = Vec::new();
        for _ in 0..1 + next_random(seed) % 9 {
            values.push(next_random(seed) % (2 * spread + 1) - spread);
        }
        values.sort();
        arrays.push(values);
    }
    arrays
}

fn main() {
    let inputs = 20;
    let rounds = 2000;
    let mut seed: i64 = 624;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..inputs {
        let spread = 1000 + next_random(&mut seed) % 9001;
        all.push(random_arrays(20000, spread, &mut seed));
    }
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let d = max_distance(&all[((r * 7) % inputs) as usize]);
        sum += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    println!("{} inputs, {} rounds: total {}, checksum {}", inputs, rounds, sum, checksum);
}
