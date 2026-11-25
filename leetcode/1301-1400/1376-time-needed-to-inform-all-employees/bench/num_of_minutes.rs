// LeetCode #1376 bench -- Rust: the ★ arm: each manager's reports in a
// list, then a breadth-first walk down from the head, each employee
// hearing the news when the manager heard it plus the manager's inform
// time.

use std::collections::VecDeque;

fn num_of_minutes(n: i32, head_id: i32, manager: &[i32], inform_time: &[i32]) -> i32 {
    let n = n as usize;
    let mut reports: Vec<Vec<usize>> = vec![Vec::new(); n];
    for (i, &m) in manager.iter().enumerate() {
        if m >= 0 {
            reports[m as usize].push(i);
        }
    }
    let mut heard = vec![0i32; n];
    let mut queue: VecDeque<usize> = VecDeque::new();
    queue.push_back(head_id as usize);
    let mut latest = 0;
    while let Some(u) = queue.pop_front() {
        latest = latest.max(heard[u]);
        for &v in &reports[u] {
            heard[v] = heard[u] + inform_time[u];
            queue.push_back(v);
        }
    }
    latest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 companies of 10^5 employees, the constraints' most, built once:
    // labelled in a random order, each employee after the first reporting
    // to any taken before it, a manager taking 1 to 1000 minutes; then
    // 200 rounds, each giving one employee of one company, both drawn
    // from the checksum so far, a new inform time if it is a manager, and
    // timing that company
    let n = 100000i64;
    let mut seed = 1376i64;
    let mut heads: Vec<i32> = Vec::new();
    let mut managers: Vec<Vec<i32>> = Vec::new();
    let mut informs: Vec<Vec<i32>> = Vec::new();
    for _ in 0..10 {
        let mut order: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            order.swap(i as usize, j as usize);
        }
        let mut manager = vec![-1i32; n as usize];
        let mut inform = vec![0i32; n as usize];
        for k in 1..n {
            let m = order[(next_random(&mut seed) % k) as usize] as usize;
            manager[order[k as usize] as usize] = m as i32;
            if inform[m] == 0 {
                inform[m] = (1 + next_random(&mut seed) % 1000) as i32;
            }
        }
        heads.push(order[0] as i32);
        managers.push(manager);
        informs.push(inform);
    }
    let mut check: i64 = 0;
    for r in 0..200i64 {
        let c = (check % 10) as usize;
        let e = ((check / 10) % n) as usize;
        let inform = &mut informs[c];
        if inform[e] > 0 {
            inform[e] = (1 + (check + r) % 1000) as i32;
        }
        let got = num_of_minutes(n as i32, heads[c], &managers[c], &informs[c]) as i64;
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("200 rounds over 10 companies of 100000 employees: checksum {check}");
}
