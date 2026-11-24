// LeetCode #1335 bench, Rust mirror of the Kāra bench: the ★ arm on 20
// schedules of 300 jobs built once, then 30 passes, each setting one job
// of every schedule and the number of days from the checksum so far,
// answering every schedule.

fn min_difficulty(job_difficulty: &[i32], d: i32) -> i32 {
    let n = job_difficulty.len();
    let days = d as usize;
    if n < days {
        return -1;
    }
    let far = i64::MAX / 2;
    let mut best: Vec<i64> = vec![far; n + 1];
    best[0] = 0;
    for day in 1..days + 1 {
        let mut next: Vec<i64> = vec![far; n + 1];
        for i in day..n + 1 {
            let mut hardest: i64 = 0;
            for j in (day - 1..i).rev() {
                hardest = hardest.max(job_difficulty[j] as i64);
                next[i] = next[i].min(best[j] + hardest);
            }
        }
        best = next;
    }
    best[n] as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 300i64;
    let mut seed = 1335i64;
    let mut schedules: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        let mut jobs: Vec<i32> = Vec::new();
        for _ in 0..n {
            jobs.push((next_random(&mut seed) % 1001) as i32);
        }
        schedules.push(jobs);
    }
    let mut check: i64 = 0;
    for pass in 0..30i64 {
        let d = (6 + check % 5) as i32;
        for t in 0..20 {
            let at = (check % n) as usize;
            schedules[t][at] = (check / 3 % 1001) as i32;
            let answer = min_difficulty(&schedules[t], d);
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("30 passes over 20 schedules of 300 jobs: checksum {}", check);
}
