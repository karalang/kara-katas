// LeetCode #2107: Number of Unique Flavors After Sharing K Candies -- the
// benchmark, the same algorithm as flavors.kara: a `HashMap` of the kept
// flavors' counts, the shared window sliding right one candy at a time.
use std::collections::HashMap;

fn share_candies(candies: &[i64], k: usize) -> i64 {
    let mut kept: HashMap<i64, i64> = HashMap::new();
    for &c in candies {
        *kept.entry(c).or_insert(0) += 1;
    }
    for &c in &candies[..k] {
        *kept.get_mut(&c).unwrap() -= 1;
    }
    let mut distinct = kept.values().filter(|&&n| n > 0).count() as i64;
    let mut best = distinct;
    for i in k..candies.len() {
        let e = kept.get_mut(&candies[i]).unwrap();
        *e -= 1;
        if *e == 0 {
            distinct -= 1;
        }
        let e = kept.get_mut(&candies[i - k]).unwrap();
        *e += 1;
        if *e == 1 {
            distinct += 1;
        }
        best = best.max(distinct);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2107;
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let flavors = next_random(&mut seed) % 5000 + 1;
        let candies: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % flavors + 1).collect();
        rows.push(candies);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for candies in &rows {
        for _ in 0..5 {
            let hi = next_random(&mut seed);
            let k = (hi * 32768 + next_random(&mut seed)) % 100001;
            let got = share_candies(candies, k as usize);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("100 shares: {} flavors kept, checksum {}", total, check);
}
