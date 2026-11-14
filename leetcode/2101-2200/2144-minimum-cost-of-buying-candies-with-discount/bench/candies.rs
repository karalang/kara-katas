// LeetCode #2144: Minimum Cost of Buying Candies With Discount -- the
// benchmark, the same algorithm as candies.kara.

fn minimum_cost(cost: &[i64]) -> i64 {
    let mut dearest_first = cost.to_vec();
    dearest_first.sort_by(|a, b| b.cmp(a));
    dearest_first.iter().enumerate().filter(|(i, _)| i % 3 != 2).map(|(_, &c)| c).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2144;
    let mut baskets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let cost: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 100 + 1).collect();
        baskets.push(cost);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..100 {
        for b in 0..1000 {
            let at = (next_random(&mut seed) % 100) as usize;
            baskets[b][at] = next_random(&mut seed) % 100 + 1;
            let paid = minimum_cost(&baskets[b]);
            total += paid;
            check = (check * 31 + paid + round) % 1000000007;
        }
    }
    println!("100000 solves: {} paid in all, checksum {}", total, check);
}
