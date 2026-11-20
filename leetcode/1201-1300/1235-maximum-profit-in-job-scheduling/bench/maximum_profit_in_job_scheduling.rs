// LeetCode #1235 bench: the ★ arm in Rust, over the same 20 sets of 50000
// jobs and 10 passes as the Kāra bench.

fn job_scheduling(start_time: &[i64], end_time: &[i64], profit: &[i64]) -> i64 {
    let n = start_time.len();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| end_time[i]);
    let ends: Vec<i64> = order.iter().map(|&i| end_time[i]).collect();
    let mut best = vec![0i64; n + 1];
    for k in 0..n {
        let job = order[k];
        let before = ends.partition_point(|&e| e <= start_time[job]);
        best[k + 1] = best[k].max(best[before] + profit[job]);
    }
    best[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1235;
    let mut sets: Vec<(Vec<i64>, Vec<i64>, Vec<i64>)> = Vec::new();
    for t in 0..20 {
        let long = 1000000 * (t % 4 + 1);
        let (mut start, mut end, mut profit) = (Vec::new(), Vec::new(), Vec::new());
        for _ in 0..50000 {
            let a = next_random(&mut seed) * 32768;
            let s = (a + next_random(&mut seed)) % 999000000 + 1;
            start.push(s);
            let b = next_random(&mut seed) * 32768;
            end.push(s + (b + next_random(&mut seed)) % long + 1);
            profit.push(next_random(&mut seed) % 10000 + 1);
        }
        sets.push((start, end, profit));
    }
    let mut check = 0;
    for _ in 0..10 {
        for (start, end, profit) in sets.iter() {
            check = (check * 131 + job_scheduling(start, end, profit)) % 1000000007;
        }
    }
    println!("20 sets of 50000 jobs, 10 passes: checksum {check}");
}
