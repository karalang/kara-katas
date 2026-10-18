// LeetCode 755 — Pour Water, bench: the ★ arm (one drop at a time),
// mirrored from pour_water.kara.

fn pour_water(heights: &[i64], volume: i64, k: i64) -> Vec<i64> {
    let mut h = heights.to_vec();
    let n = h.len() as i64;
    for _ in 0..volume {
        let mut best = k;
        for d in [-1i64, 1] {
            let mut i = k;
            while i + d >= 0 && i + d < n && h[(i + d) as usize] <= h[i as usize] {
                if h[(i + d) as usize] < h[best as usize] {
                    best = i + d;
                }
                i += d;
            }
            if best != k {
                break;
            }
        }
        h[best as usize] += 1;
    }
    h
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 6000;
    let mut seed: i64 = 755;
    let mut water: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut heights: Vec<i64> = Vec::new();
        for _ in 0..100 {
            heights.push(next_random(&mut seed) % 100);
        }
        let volume = 2000;
        let k = next_random(&mut seed) % 100;
        let after = pour_water(&heights, volume, k);
        for &x in after.iter() {
            water += x;
            check = (check * 31 + x) % 1000000007;
        }
    }
    println!("{} landscapes of 100 columns, 2000 drops each: {} units in all, checksum {}", rounds, water, check);
}
