// LeetCode #2398: Maximum Number of Robots Within Budget -- the bench, the
// ★ arm in Rust: a sliding window, its largest charge time kept by a
// monotonic deque.

use std::collections::VecDeque;

fn maximum_robots(charge_times: &[i64], running_costs: &[i64], budget: i64) -> i64 {
    let mut best = 0i64;
    let mut left = 0usize;
    let mut sum = 0i64;
    let mut largest: VecDeque<usize> = VecDeque::new();
    for right in 0..charge_times.len() {
        sum += running_costs[right];
        while let Some(&back) = largest.back() {
            if charge_times[back] <= charge_times[right] {
                largest.pop_back();
            } else {
                break;
            }
        }
        largest.push_back(right);
        while left <= right && charge_times[largest[0]] + (right - left + 1) as i64 * sum > budget {
            if largest[0] == left {
                largest.pop_front();
            }
            sum -= running_costs[left];
            left += 1;
        }
        best = best.max((right + 1 - left) as i64);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2398i64;
    let mut fleets = Vec::new();
    for _ in 0..20 {
        let charge: Vec<i64> = (0..50000).map(|_| 1 + wide(&mut seed) % 100000).collect();
        let running: Vec<i64> = (0..50000).map(|_| 1 + wide(&mut seed) % 100000).collect();
        fleets.push((charge, running));
    }
    let mut check = 0i64;
    for p in 0..2i64 {
        for (charge, running) in &fleets {
            let mut budget = 100000i64;
            while budget <= 1000000000000000 {
                check = (check * 31 + maximum_robots(charge, running, budget) + p) % 1000000007;
                budget *= 10;
            }
        }
    }
    println!("2 passes over 20 fleets of 5 * 10^4 robots, 11 budgets: checksum {}", check);
}
