// Benchmark for #826: Most Profit Assigning Work -- the ★ arm (two sorted sweeps).
//
// Mirrors max_profit_assignment.kara: the jobs paired and sorted by
// difficulty (then profit) and a copy of the workers sorted, then one
// pointer walks the jobs as the abilities grow, keeping the best profit
// among the jobs passed.

fn max_profit_assignment(difficulty: &[i64], profit: &[i64], worker: &[i64]) -> i64 {
    let n = difficulty.len();
    let mut jobs: Vec<(i64, i64)> = Vec::new();
    for i in 0..n {
        jobs.push((difficulty[i], profit[i]));
    }
    jobs.sort();
    let mut abilities = worker.to_vec();
    abilities.sort();
    let mut next = 0;
    let mut best = 0;
    let mut total = 0;
    for &ability in &abilities {
        while next < n && jobs[next].0 <= ability {
            best = best.max(jobs[next].1);
            next += 1;
        }
        total += best;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, count: usize) -> Vec<i64> {
    (0..count).map(|_| 1 + next_random(seed) % 100000).collect()
}

fn main() {
    let count = 64usize;
    let rounds = 2000usize;
    let mut seed: i64 = 826;
    let mut difficulties = Vec::new();
    let mut profits = Vec::new();
    let mut workers = Vec::new();
    for _ in 0..count {
        difficulties.push(draw(&mut seed, 10000));
        profits.push(draw(&mut seed, 10000));
        workers.push(draw(&mut seed, 10000));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let r = max_profit_assignment(&difficulties[g], &profits[g], &workers[g]);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    println!("{rounds} rounds of {count} cases: total {total}, checksum {checksum}");
}
