// Benchmark for #514: Rust mirror of the ★ arm (a cost per position of
// the current letter); see find_rotate_steps.kara.

fn find_rotate_steps(ring: &[u8], key: &[u8]) -> i64 {
    let n = ring.len() as i64;
    let mut at: Vec<Vec<i64>> = vec![Vec::new(); 26];
    for j in 0..ring.len() {
        at[(ring[j] - b'a') as usize].push(j as i64);
    }
    let mut prev_pos: Vec<i64> = vec![0];
    let mut prev_cost: Vec<i64> = vec![0];
    for &c in key {
        let pos = at[(c - b'a') as usize].clone();
        let mut cost: Vec<i64> = Vec::new();
        for q in pos.iter() {
            let mut best = i64::MAX;
            for i in 0..prev_pos.len() {
                let d = (prev_pos[i] - *q).abs();
                best = best.min(prev_cost[i] + d.min(n - d));
            }
            cost.push(best);
        }
        prev_pos = pos;
        prev_cost = cost;
    }
    let mut fewest = i64::MAX;
    for c in prev_cost.iter() {
        fewest = fewest.min(*c);
    }
    fewest + key.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 400 random rings of 300 letters from all 26, each with a key of
    // 2,000 letters drawn from the ring, solved once each.
    let mut seed: i64 = 514;
    let rings = 400;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rings {
        let mut ring: Vec<u8> = Vec::new();
        for _ in 0..300 {
            ring.push(b'a' + (next_random(&mut seed) % 26) as u8);
        }
        let mut key: Vec<u8> = Vec::new();
        for _ in 0..2000 {
            key.push(ring[(next_random(&mut seed) % 300) as usize]);
        }
        let steps = find_rotate_steps(&ring, &key);
        total += steps;
        checksum = (checksum * 31 + steps) % 1000000007;
    }
    println!("{} rings of 300 letters, keys of 2000: {} steps in all, checksum {}", rings, total, checksum);
}
