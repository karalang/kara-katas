// LeetCode #875 bench: Rust mirror of min_eating_speed.kara (the ★ arm,
// binary search on the speed) on the same 600 searches.

fn min_eating_speed(piles: &[i64], h: i64) -> i64 {
    let mut lo = 1;
    let mut hi = 1;
    for &p in piles {
        hi = hi.max(p);
    }
    while lo < hi {
        let k = (lo + hi) / 2;
        if hours(piles, k) <= h {
            hi = k;
        } else {
            lo = k + 1;
        }
    }
    lo
}

fn hours(piles: &[i64], k: i64) -> i64 {
    let mut total = 0;
    for &p in piles {
        total += (p + k - 1) / k;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn up_to(seed: &mut i64, limit: i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    (a * 32768 + b) % limit + 1
}

fn main() {
    let mut seed = 875;
    let mut pile_sets: Vec<Vec<i64>> = Vec::new();
    for k in 0..20 {
        let limit = if k % 2 == 0 { 1000000000 } else { 1000000 };
        let mut piles = Vec::new();
        for _ in 0..10000 {
            piles.push(up_to(&mut seed, limit));
        }
        pile_sets.push(piles);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for k in 0..600 {
        let h = 10000 + up_to(&mut seed, if k % 3 == 0 { 1000000000 - 10000 } else { 1000000 }) - 1;
        let answer = min_eating_speed(&pile_sets[k % 20], h);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("600 searches over 10000 piles: speeds sum to {}, checksum {}", total, check);
}
