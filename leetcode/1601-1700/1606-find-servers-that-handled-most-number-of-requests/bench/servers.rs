// LeetCode #1606: Find Servers That Handled Most Number of Requests -- the
// bench in Rust, mirroring servers.kara: the free servers in a BTreeSet,
// the busy ones in a BinaryHeap of Reverse((time free, server)).
use std::cmp::Reverse;
use std::collections::{BTreeSet, BinaryHeap};

fn busiest_servers(k: i32, arrival: &[i32], load: &[i32]) -> Vec<i32> {
    let mut free: BTreeSet<i32> = (0..k).collect();
    let mut busy: BinaryHeap<Reverse<(i64, i32)>> = BinaryHeap::new();
    let mut handled = vec![0; k as usize];
    for i in 0..arrival.len() {
        let now = arrival[i] as i64;
        while let Some(&Reverse((t, _))) = busy.peek() {
            if t > now {
                break;
            }
            let Reverse((_, s)) = busy.pop().unwrap();
            free.insert(s);
        }
        let start = (i % k as usize) as i32;
        let pick = free.range(start..).next().or(free.first()).copied();
        if let Some(s) = pick {
            free.remove(&s);
            busy.push(Reverse((now + load[i] as i64, s)));
            handled[s as usize] += 1;
        }
    }
    let most = *handled.iter().max().unwrap();
    (0..k).filter(|&s| handled[s as usize] == most).collect()
}

fn main() {
    let mut seed: i64 = 1606;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut problems: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..20 {
        let mut arrival = Vec::new();
        let mut load = Vec::new();
        let mut t: i64 = 0;
        for _ in 0..100000 {
            t += next_random() % 3 + 1;
            arrival.push(t as i32);
            let a = next_random();
            let b = next_random();
            load.push(((a * 32768 + b) % 30000 + 1) as i32);
        }
        problems.push((arrival, load));
    }
    let mut check: i64 = 0;
    let mut busiest = 0;
    for (arrival, load) in &problems {
        let servers = busiest_servers(10000, arrival, load);
        for &s in &servers {
            check = (check * 31 + s as i64 + 1) % 1000000007;
        }
        busiest += servers.len();
    }
    println!("20 problems of 10000 servers and 100000 requests: {busiest} busiest, checksum {check}");
}
