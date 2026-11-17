// LeetCode #2244: Minimum Rounds to Complete All Tasks -- the benchmark's
// Rust mirror of rounds.kara: the tasks of each difficulty counted in a
// `HashMap`; a lone task gives -1, any other count c takes ceil(c / 3)
// rounds, summed.
use std::collections::HashMap;

fn minimum_rounds(tasks: &[i64]) -> i64 {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &t in tasks {
        *counts.entry(t).or_insert(0) += 1;
    }
    let mut rounds = 0;
    for &c in counts.values() {
        if c == 1 {
            return -1;
        }
        rounds += (c + 2) / 3;
    }
    rounds
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2244i64;
    let mut check = 0i64;
    for _ in 0..40 {
        let kinds: Vec<i64> = (0..30000).map(|_| wide_random(&mut seed) % 1000000000 + 1).collect();
        let mut tasks: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let t = kinds[(wide_random(&mut seed) % 30000) as usize];
            tasks.push(t);
            tasks.push(t);
        }
        check = (check * 31 + minimum_rounds(&tasks) + 1) % 1000000007;
    }
    println!("40 lists of 100000 tasks: checksum {}", check);
}
