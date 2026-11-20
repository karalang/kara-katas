// LeetCode #1723: Find Minimum Time to Finish All Jobs -- the bench
// (jobs.kara): each job, the longest first, tried on every worker by
// backtracking, a branch cut once it cannot beat the best finish found,
// and only the first idle worker tried.

fn place(jobs: &[i32], i: usize, loads: &mut Vec<i32>, best: &mut i32) {
    if i == jobs.len() {
        *best = *loads.iter().max().unwrap();
        return;
    }
    for w in 0..loads.len() {
        if loads[w] + jobs[i] < *best {
            loads[w] += jobs[i];
            place(jobs, i + 1, loads, best);
            loads[w] -= jobs[i];
        }
        if loads[w] == 0 {
            break;
        }
    }
}

fn minimum_time_required(jobs: &[i32], k: i32) -> i32 {
    let mut order = jobs.to_vec();
    order.sort_by(|a, b| b.cmp(a));
    let total: i32 = order.iter().sum();
    let mut loads = vec![0i32; k as usize];
    let mut best = total + 1;
    place(&order, 0, &mut loads, &mut best);
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let count = 100;
    let rounds: i64 = 5;
    let n = 12;
    let mut seed: i64 = 1723;
    let mut problems: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..count {
        let jobs: Vec<i32> = (0..n)
            .map(|_| (wide(&mut seed) % 10000000 + 1) as i32)
            .collect();
        let k = (next_random(&mut seed) % 11 + 2) as i32;
        problems.push((jobs, k));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (jobs, k) in problems.iter() {
            let answer = minimum_time_required(jobs, *k) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} problems of {} jobs, {} rounds: answers sum to {}, checksum {}",
        count, n, rounds, sum, check
    );
}
