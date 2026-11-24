// LeetCode #1298 bench: the ★ arm (a breadth-first walk over the boxes that
// can be opened, each queued once, when it is both held and open) over 100
// cases of 1000 boxes, built once; then 5000 passes, each flipping one box of
// every case between open and locked, chosen from the checksum so far,
// answering it, and folding the answer into the checksum.
use std::collections::VecDeque;

fn max_candies(status: &[i64], candies: &[i64], keys: &[Vec<i64>], contained_boxes: &[Vec<i64>], initial_boxes: &[i64]) -> i64 {
    let n = status.len();
    let mut open: Vec<bool> = status.iter().map(|&s| s == 1).collect();
    let mut held = vec![false; n];
    let mut queued = vec![false; n];
    let mut queue: VecDeque<i64> = VecDeque::new();
    for &b in initial_boxes {
        let b = b as usize;
        held[b] = true;
        if open[b] && !queued[b] {
            queued[b] = true;
            queue.push_back(b as i64);
        }
    }
    let mut total = 0;
    while let Some(b) = queue.pop_front() {
        let b = b as usize;
        total += candies[b];
        for &k in &keys[b] {
            let k = k as usize;
            open[k] = true;
            if held[k] && !queued[k] {
                queued[k] = true;
                queue.push_back(k as i64);
            }
        }
        for &c in &contained_boxes[b] {
            let c = c as usize;
            held[c] = true;
            if open[c] && !queued[c] {
                queued[c] = true;
                queue.push_back(c as i64);
            }
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct Case {
    status: Vec<i64>,
    candies: Vec<i64>,
    keys: Vec<Vec<i64>>,
    contained: Vec<Vec<i64>>,
    initial: Vec<i64>,
}

fn make_case(seed: &mut i64, n: i64, open: i64, initial_in: i64, nest: i64, max_keys: i64) -> Case {
    let mut order: Vec<i64> = (0..n).collect();
    for i in 0..n {
        let j = i + next_random(seed) % (n - i);
        order.swap(i as usize, j as usize);
    }
    let nu = n as usize;
    let mut status = vec![0i64; nu];
    let mut candies = vec![0i64; nu];
    let mut keys: Vec<Vec<i64>> = vec![Vec::new(); nu];
    let mut contained: Vec<Vec<i64>> = vec![Vec::new(); nu];
    let mut initial: Vec<i64> = Vec::new();
    for i in 0..n {
        let b = order[i as usize] as usize;
        let roll = next_random(seed) % 100;
        if i > 0 && roll < nest {
            let parent = order[(next_random(seed) % i) as usize] as usize;
            contained[parent].push(b as i64);
        } else if next_random(seed) % 100 < initial_in {
            initial.push(b as i64);
        }
        if next_random(seed) % 100 < open {
            status[b] = 1;
        }
        candies[b] = 1 + next_random(seed) % 1000;
        let count = next_random(seed) % (max_keys + 1);
        for _ in 0..count {
            let k = next_random(seed) % n;
            if !keys[b].contains(&k) {
                keys[b].push(k);
            }
        }
    }
    Case { status, candies, keys, contained, initial }
}

fn main() {
    let mut seed = 1298;
    let mut cases: Vec<Case> = Vec::new();
    for t in 0..100 {
        cases.push(make_case(&mut seed, 1000, 10 + t % 40, 5 + t % 20, 60 + t % 40, 1 + t % 4));
    }
    let mut check: i64 = 0;
    for p in 0..5000 {
        for c in cases.iter_mut() {
            let b = (check % 1000) as usize;
            c.status[b] = 1 - c.status[b];
            let got = max_candies(&c.status, &c.candies, &c.keys, &c.contained, &c.initial);
            check = (check * 31 + got + p) % 1000000007;
        }
    }
    println!("5000 passes over 100 cases of 1000 boxes: checksum {}", check);
}
