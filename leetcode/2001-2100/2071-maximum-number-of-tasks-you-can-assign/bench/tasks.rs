// LeetCode #2071: Maximum Number of Tasks You Can Assign -- Rust mirror of
// the ★ arm's benchmark (tasks.kara): 12 problems of 50000 tasks and 50000
// workers, strengths up to 1000000000, 0 to 11000 pills of strength
// 10000000.

use std::collections::VecDeque;

fn can_do(tasks: &[i64], workers: &[i64], k: usize, pills: i64, strength: i64) -> bool {
    let mut left = pills;
    let mut waiting: VecDeque<i64> = VecDeque::new();
    let mut next = 0;
    for &w in &workers[workers.len() - k..] {
        while next < k && tasks[next] <= w + strength {
            waiting.push_back(tasks[next]);
            next += 1;
        }
        match waiting.front() {
            None => return false,
            Some(&easiest) if easiest <= w => {
                waiting.pop_front();
            }
            Some(_) => {
                if left == 0 {
                    return false;
                }
                left -= 1;
                waiting.pop_back();
            }
        }
    }
    true
}

fn max_task_assign(tasks: &[i64], workers: &[i64], pills: i64, strength: i64) -> i64 {
    let mut tasks = tasks.to_vec();
    let mut workers = workers.to_vec();
    tasks.sort();
    workers.sort();
    let (mut lo, mut hi) = (0, tasks.len().min(workers.len()));
    while lo < hi {
        let mid = (lo + hi + 1) / 2;
        if can_do(&tasks, &workers, mid, pills, strength) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn strengths(n: usize, low: i64, high: i64, seed: &mut i64) -> Vec<i64> {
    let mut out = Vec::new();
    for _ in 0..n {
        let a = next_random(seed);
        let b = next_random(seed);
        out.push(low + (a * 32768 + b) % (high - low + 1));
    }
    out
}

fn main() {
    let mut seed = 2071;
    let mut total = 0;
    let mut check = 0;
    for t in 0..12 {
        let tasks = strengths(50000, 0, 1000000000, &mut seed);
        let workers = strengths(50000, 0, 1000000000, &mut seed);
        let a = max_task_assign(&tasks, &workers, t * 1000, 10000000);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("12 problems: sum {}, checksum {}", total, check);
}
