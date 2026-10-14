// Benchmark for #575: Rust mirror of the ★ arm (a set of the types); see
// distribute_candies.kara. A fresh `HashSet<i64>` with the default hasher
// for every call, as the Kāra arm makes a fresh `Set[i64]`.

use std::collections::HashSet;

fn distribute_candies(candy_type: &[i64]) -> i64 {
    let mut kinds: HashSet<i64> = HashSet::new();
    for c in candy_type.iter() {
        kinds.insert(*c);
    }
    (kinds.len() as i64).min(candy_type.len() as i64 / 2)
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 100;
    let rounds: i64 = 200;
    let mut seed: i64 = 575;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let types = 1 + next_random(&mut seed) % 10000;
        let mut pool: Vec<i64> = Vec::new();
        for _ in 0..types {
            let high = next_random(&mut seed) * 32768;
            pool.push((high + next_random(&mut seed)) % 200001 - 100000);
        }
        let mut candies: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            candies.push(pool[(next_random(&mut seed) % types) as usize]);
        }
        cases.push(candies);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let got = distribute_candies(&cases[p]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} cases of 10000 candies, {} rounds: {} types eaten, checksum {}", count, rounds, total, checksum);
}
