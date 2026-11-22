// LeetCode #2819: Minimum Relative Loss After Buying Chocolates -- the
// bench's Rust mirror of the ★ arm: the prices sorted, prefix sums, and
// a binary search per query for how many come from the cheap end.

fn minimum_relative_losses(prices: &[i64], queries: &[[i64; 2]]) -> Vec<i64> {
    let mut sorted = prices.to_vec();
    sorted.sort();
    let n = sorted.len();
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + sorted[i];
    }
    let mut out = Vec::new();
    for q in queries {
        let (k, m) = (q[0], q[1] as usize);
        let (mut lo, mut hi) = (0usize, m);
        while lo < hi {
            let mid = (lo + hi) / 2;
            if sorted[mid] + sorted[n - m + mid] < 2 * k {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        let dear = prefix[n] - prefix[n - m + lo];
        out.push(prefix[lo] + 2 * k * (m - lo) as i64 - dear);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n: i64 = 100000;
    let mut seed = 2819;
    let mut shops: Vec<(Vec<i64>, Vec<[i64; 2]>)> = Vec::new();
    for _ in 0..count {
        let prices: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        let queries: Vec<[i64; 2]> = (0..n)
            .map(|_| {
                let k = wide(&mut seed) % 1000000000 + 1;
                [k, wide(&mut seed) % n + 1]
            })
            .collect();
        shops.push((prices, queries));
    }
    let mut negative = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (prices, queries) in &shops {
            for a in minimum_relative_losses(prices, queries) {
                if a < 0 {
                    negative += 1;
                }
                check = ((check * 31 + a + r) % 1000000007 + 1000000007) % 1000000007;
            }
        }
    }
    println!("{} shops of {}, {} rounds: {} losses below 0, checksum {}", count, n, rounds, negative, check);
}
