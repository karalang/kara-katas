// Benchmark for #358 -- mirror of rearrange.kara.
use std::collections::{BinaryHeap, VecDeque};

fn rearrange(s: &[u8], k: i64) -> Vec<u8> {
    let mut counts = [0i64; 26];
    for &b in s {
        counts[(b - b'a') as usize] += 1;
    }
    // (copies left, -letter): the largest pops first.
    let mut ready: BinaryHeap<(i64, i64)> = BinaryHeap::new();
    for c in 0..26 {
        if counts[c] > 0 {
            ready.push((counts[c], -(c as i64)));
        }
    }
    let mut cooling: VecDeque<(i64, i64)> = VecDeque::new();
    let mut out = Vec::with_capacity(s.len());
    for _ in 0..s.len() {
        match ready.pop() {
            Some((left, neg)) => {
                let c = -neg;
                out.push(c as u8 + b'a');
                cooling.push_back((left - 1, c));
            }
            None => return Vec::new(),
        }
        if cooling.len() as i64 >= k {
            if let Some((left, c)) = cooling.pop_front() {
                if left > 0 {
                    ready.push((left, -c));
                }
            }
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 358;
    let mut possible = 0;
    let mut checksum: i64 = 0;
    for _ in 0..200 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let width = (seed / 65536) % 23 + 4;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = (seed / 65536) % 8 + 1;
        let mut s = Vec::with_capacity(50000);
        for _ in 0..50000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let draw = seed / 65536;
            let c = if draw % 8 == 0 { 0 } else { (draw / 8) % width };
            s.push(c as u8 + b'a');
        }
        let r = rearrange(&s, k);
        if r.len() == s.len() {
            possible += 1;
        }
        for &b in &r {
            checksum = (checksum * 31 + b as i64) % 1000000007;
        }
        checksum = (checksum * 31 + 7) % 1000000007;
    }
    println!("{} of 200 strings can be arranged, checksum {}", possible, checksum);
}
