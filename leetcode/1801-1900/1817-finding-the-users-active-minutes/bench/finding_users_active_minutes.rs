// LeetCode #1817: Finding the Users Active Minutes -- the bench in Rust:
// the ★ arm over 5000 calls on runs of 5000 to 9999 logs cut from one list
// of 10^4 logs over 1000 users and 100 minutes, built once, each run's
// length drawn from the checksum so far.
use std::collections::{HashMap, HashSet};

fn finding_users_active_minutes(logs: Vec<Vec<i64>>, k: i64) -> Vec<i64> {
    let mut minutes: HashMap<i64, HashSet<i64>> = HashMap::new();
    for log in logs.iter() {
        minutes.entry(log[0]).or_insert_with(HashSet::new).insert(log[1]);
    }
    let mut answer = vec![0i64; k as usize];
    for seen in minutes.values() {
        answer[seen.len() - 1] += 1;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1817;
    let mut base: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10000 {
        let user = next_random(&mut seed) % 1000;
        base.push(vec![user, next_random(&mut seed) % 100]);
    }
    let mut check: i64 = 0;
    for call in 0..5000i64 {
        let n = (5000 + (check + call) % 5000) as usize;
        for x in finding_users_active_minutes(base[..n].to_vec(), 100) {
            check = (check * 31 + x) % 1000000007;
        }
    }
    println!("5000 calls: checksum {}", check);
}
