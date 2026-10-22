// Benchmark for #854: K-Similar Strings -- Rust twin of the Kāra ★ arm
// (breadth-first search over swaps that fix a letter).
use std::collections::HashSet;

fn k_similarity(s1: &str, s2: &str) -> i64 {
    let goal = s2.as_bytes();
    let n = goal.len();
    let mut seen: HashSet<String> = HashSet::new();
    let mut level: Vec<Vec<u8>> = vec![s1.as_bytes().to_vec()];
    seen.insert(s1.to_string());
    let mut swaps = 0;
    loop {
        let mut next: Vec<Vec<u8>> = Vec::new();
        for cur in level.iter() {
            let mut i = 0;
            while i < n && cur[i] == goal[i] {
                i += 1;
            }
            if i == n {
                return swaps;
            }
            for j in i + 1..n {
                if cur[j] == goal[i] && cur[j] != goal[j] {
                    let mut moved = cur.clone();
                    moved.swap(i, j);
                    let key = String::from_utf8(moved.clone()).unwrap();
                    if !seen.contains(&key) {
                        seen.insert(key);
                        next.push(moved);
                    }
                }
            }
        }
        level = next;
        swaps += 1;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 64;
    let rounds = 6400;
    let n = 20;
    let mut seed: i64 = 854;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for g in 0..count {
        let letters = 2 + (g % 5) as i64;
        let mut a: Vec<u8> = Vec::new();
        for _ in 0..n {
            a.push(b'a' + (next_random(&mut seed) % letters) as u8);
        }
        let mut b = a.clone();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            b.swap(i, j);
        }
        firsts.push(String::from_utf8(a).unwrap());
        seconds.push(String::from_utf8(b).unwrap());
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let k = k_similarity(&firsts[g], &seconds[g]);
        total += k;
        checksum = (checksum * 31 + k) % 1000000007;
    }
    println!("{} rounds of {} pairs: swaps sum to {}, checksum {}", rounds, count, total, checksum);
}
