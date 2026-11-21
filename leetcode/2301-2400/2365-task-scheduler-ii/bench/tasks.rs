// LeetCode #2365: Task Scheduler II -- the bench, the ★ arm in Rust: the
// day goes forward one for each task, and jumps to the day after the
// type's last run plus `space` when that is later; a `HashMap` keeps each
// type's last day.

use std::collections::HashMap;

fn task_scheduler_ii(tasks: &[i64], space: i64) -> i64 {
    let mut last: HashMap<i64, i64> = HashMap::new();
    let mut day = 0i64;
    for &task in tasks {
        day += 1;
        if let Some(&before) = last.get(&task) {
            day = day.max(before + space + 1);
        }
        last.insert(task, day);
    }
    day
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    // list a: 10^5 tasks of 4^(a / 2 + 1) types (at most 10^5) up to
    // 10^9, with a space of 3^a
    let mut seed = 2365i64;
    let mut lists: Vec<(Vec<i64>, i64)> = Vec::new();
    let mut space = 1i64;
    for a in 0..10 {
        let kinds = (1i64 << (2 * (a / 2 + 1))).min(100000);
        let types: Vec<i64> = (0..kinds).map(|_| 1 + wide_random(&mut seed) % 1000000000).collect();
        let tasks: Vec<i64> = (0..100000).map(|_| types[(wide_random(&mut seed) % kinds) as usize]).collect();
        lists.push((tasks, space));
        space *= 3;
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for (tasks, space) in &lists {
            check = (check * 31 + task_scheduler_ii(tasks, *space) % 1000000007 + p) % 1000000007;
        }
    }
    println!("20 passes over 10 lists of 10^5 tasks: checksum {}", check);
}
