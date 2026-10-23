// LeetCode #871: Minimum Number of Refueling Stops -- Rust mirror of the
// bench program (the ★ arm, a heap of the stations passed), with a
// `BinaryHeap` as the Kāra program has a max-first `PriorityQueue`.

use std::collections::BinaryHeap;

fn min_refuel_stops(target: i64, start_fuel: i64, stations: &[(i64, i64)]) -> i64 {
    let mut passed = BinaryHeap::new();
    let mut reach = start_fuel;
    let mut stops = 0;
    let mut next = 0;
    while reach < target {
        while next < stations.len() && stations[next].0 <= reach {
            passed.push(stations[next].1);
            next += 1;
        }
        match passed.pop() {
            Some(fuel) => {
                reach += fuel;
                stops += 1;
            }
            None => return -1,
        }
    }
    stops
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_below(seed: &mut i64, limit: i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % limit
}

fn main() {
    let mut seed: i64 = 871;
    let mut total: i64 = 0;
    let mut unreachable: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..100 {
        let target = random_below(&mut seed, 500000000) + 500000001;
        let mut positions: Vec<i64> = Vec::new();
        for _ in 0..500 {
            positions.push(random_below(&mut seed, target - 1) + 1);
        }
        positions.sort();
        positions.dedup();
        let mut stations: Vec<(i64, i64)> = Vec::new();
        for &p in &positions {
            stations.push((p, random_below(&mut seed, target / 40) + 1));
        }
        for j in 0..400 {
            let a = min_refuel_stops(target, j * (target / 800) + 1, &stations);
            if a < 0 {
                unreachable += 1;
            } else {
                total += a;
            }
            check = (check * 31 + a + 1) % 1000000007;
        }
    }
    println!(
        "40000 trips over 100 lists of 500 stations: stops sum to {}, {} unreachable, checksum {}",
        total, unreachable, check
    );
}
