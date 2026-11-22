// LeetCode #2895: Minimum Processing Time -- the bench, as
// processing.kara: 20 cases of 25000 processors and 10^5 tasks, each
// answered 20 times by the sorting arm, each sorting fresh copies.

fn min_processing_time(processor_time: &[i64], tasks: &[i64]) -> i64 {
    let mut free = processor_time.to_vec();
    free.sort();
    let mut longest = tasks.to_vec();
    longest.sort();
    longest.reverse();
    let mut finish = 0;
    for (i, &p) in free.iter().enumerate() {
        finish = finish.max(p + longest[4 * i]);
    }
    finish
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (20, 20i64, 25000);
    let mut seed = 2895;
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let processors: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000).collect();
        let tasks: Vec<i64> = (0..4 * n)
            .map(|_| wide(&mut seed) % 1000000000 + 1)
            .collect();
        cases.push((processors, tasks));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (processors, tasks) in cases.iter() {
            let time = min_processing_time(processors, tasks);
            total += time;
            check = (check * 31 + time + r) % 1000000007;
        }
    }
    println!("{count} cases of {n}, {rounds} rounds: times total {total}, checksum {check}");
}
