// LeetCode 746 — Min Cost Climbing Stairs, bench: the ★ arm (two running
// totals) on a staircase of 1000 steps whose costs keep changing.
// Mirrors min_cost_climbing_stairs.kara.

fn min_cost_climbing_stairs(cost: &[i64]) -> i64 {
    let mut before = 0;
    let mut here = 0;
    for i in 2..cost.len() + 1 {
        let next = if before + cost[i - 2] < here + cost[i - 1] { before + cost[i - 2] } else { here + cost[i - 1] };
        before = here;
        here = next;
    }
    here
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 300000;
    let n = 1000;
    let mut seed = 746;
    let mut cost: Vec<i64> = Vec::new();
    for _ in 0..n {
        cost.push(next_random(&mut seed) % 1000);
    }
    let mut total: i64 = 0;
    for _ in 0..rounds {
        for _ in 0..5 {
            let i = (next_random(&mut seed) % n) as usize;
            cost[i] = next_random(&mut seed) % 1000;
        }
        total += min_cost_climbing_stairs(&cost);
    }
    println!("{} rounds on 1000 steps: least costs sum to {}", rounds, total);
}
