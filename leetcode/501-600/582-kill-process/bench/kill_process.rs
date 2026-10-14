// Benchmark for #582: Rust mirror of the ★ arm (children lists, walked
// breadth first); see kill_process.kara. A `HashMap<i64, Vec<i64>>` with
// the default hasher and a `VecDeque`, as the Kāra arm uses a `Map` and
// a `VecDeque`.

use std::collections::{HashMap, VecDeque};

fn kill_process(pid: &[i64], ppid: &[i64], kill: i64) -> Vec<i64> {
    let mut children: HashMap<i64, Vec<i64>> = HashMap::new();
    for i in 0..pid.len() {
        children.entry(ppid[i]).or_insert_with(Vec::new).push(pid[i]);
    }
    let mut killed: Vec<i64> = Vec::new();
    let mut queue: VecDeque<i64> = VecDeque::new();
    queue.push_back(kill);
    while let Some(p) = queue.pop_front() {
        killed.push(p);
        if let Some(kids) = children.get(&p) {
            for k in kids.iter() {
                queue.push_back(*k);
            }
        }
    }
    killed
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed) * 32768;
    high + next_random(seed)
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 30;
    let n: i64 = 50000;
    let mut seed: i64 = 582;
    let mut pids: Vec<Vec<i64>> = Vec::new();
    let mut ppids: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut names: Vec<i64> = (1..=n).collect();
        for i in (1..n).rev() {
            let j = wide(&mut seed) % (i + 1);
            names.swap(i as usize, j as usize);
        }
        let mut pid: Vec<i64> = Vec::new();
        let mut ppid: Vec<i64> = Vec::new();
        for i in 0..n {
            pid.push(names[i as usize]);
            if i == 0 {
                ppid.push(0);
            } else {
                ppid.push(names[(wide(&mut seed) % i) as usize]);
            }
        }
        pids.push(pid);
        ppids.push(ppid);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let kill = if (round + g) % 4 == 0 { pids[p][0] } else { pids[p][(wide(&mut seed) % n) as usize] };
            let got = kill_process(&pids[p], &ppids[p], kill);
            let mut sum: i64 = 0;
            for k in got.iter() {
                sum += *k;
            }
            total += got.len() as i64;
            checksum = (checksum * 31 + sum) % 1000000007;
        }
    }
    println!("{} trees of 50000 processes, {} rounds: {} killed, checksum {}", count, rounds, total, checksum);
}
