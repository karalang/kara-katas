// LeetCode #1834: Single-Threaded CPU -- the bench in Rust: the ★ arm over
// 50 calls on the first 50000 to 99999 of one list of 10^5 tasks, built once,
// each coming in at 1 to 10^6 and taking 1 to 10^4, each run's length drawn
// from the checksum so far. Each call copies its run, a list of two-number
// lists, as the arm takes its list by value, and the order is folded into
// the checksum.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn get_order(tasks: Vec<Vec<i64>>) -> Vec<i64> {
    let n = tasks.len();
    let mut coming: Vec<usize> = (0..n).collect();
    coming.sort_by_key(|&i| tasks[i][0]);
    let mut ready: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    let mut order: Vec<i64> = Vec::new();
    let mut clock: i64 = 0;
    let mut next = 0;
    while order.len() < n {
        if ready.is_empty() && clock < tasks[coming[next]][0] {
            clock = tasks[coming[next]][0];
        }
        while next < n && tasks[coming[next]][0] <= clock {
            let i = coming[next];
            ready.push(Reverse((tasks[i][1], i)));
            next += 1;
        }
        let Reverse((processing, i)) = ready.pop().unwrap();
        clock += processing;
        order.push(i as i64);
    }
    order
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1834;
    let mut base: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        let enqueue = 1 + (hi * 32768 + next_random(&mut seed)) % 1000000;
        let processing = 1 + next_random(&mut seed) % 10000;
        base.push(vec![enqueue, processing]);
    }
    let mut check: i64 = 0;
    for call in 0..50 {
        let n = (50000 + (check + call) % 50000) as usize;
        let order = get_order(base[..n].to_vec());
        for &i in order.iter() {
            check = (check * 31 + i + 1) % 1000000007;
        }
    }
    println!("50 calls: checksum {}", check);
}
