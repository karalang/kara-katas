// LeetCode #2050: Parallel Courses III -- Rust mirror of the ★ arm's
// benchmark (courses.kara): the same 40 graphs of 50000 courses, the same
// Kahn's topological order.
use std::collections::VecDeque;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_time(n: usize, relations: &[(usize, usize)], time: &[i64]) -> i64 {
    let mut next: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut waiting = vec![0i64; n];
    for &(a, b) in relations {
        next[a - 1].push(b - 1);
        waiting[b - 1] += 1;
    }
    let mut start = vec![0i64; n];
    let mut queue: VecDeque<usize> = VecDeque::new();
    for v in 0..n {
        if waiting[v] == 0 {
            queue.push_back(v);
        }
    }
    let mut months = 0;
    while let Some(v) = queue.pop_front() {
        let done = start[v] + time[v];
        months = months.max(done);
        for &w in &next[v] {
            start[w] = start[w].max(done);
            waiting[w] -= 1;
            if waiting[w] == 0 {
                queue.push_back(w);
            }
        }
    }
    months
}

fn main() {
    let n = 50000usize;
    let mut seed = 2050i64;
    let (mut sum, mut check) = (0i64, 0i64);
    for t in 0..40i64 {
        let reach = 1 + t * 1000;
        let mut order: Vec<usize> = (1..n + 1).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            order.swap(i, j);
        }
        let mut relations = Vec::with_capacity(n - 1);
        for i in 1..n {
            let at = i - (next_random(&mut seed) % reach.min(i as i64) + 1) as usize;
            relations.push((order[at], order[i]));
        }
        let time: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % 10000 + 1).collect();
        let months = minimum_time(n, &relations, &time);
        sum += months;
        check = (check * 31 + months) % 1000000007;
    }
    println!("40 graphs: sum {}, checksum {}", sum, check);
}
