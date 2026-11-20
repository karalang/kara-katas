// LeetCode #1231 bench: the ★ arm in Rust, over the same 100 random bars
// and 20 passes as the Kāra bench.

fn pieces(sweetness: &[i64], m: i64) -> i64 {
    let mut count = 0;
    let mut piece = 0;
    for &s in sweetness {
        piece += s;
        if piece >= m {
            count += 1;
            piece = 0;
        }
    }
    count
}

fn maximize_sweetness(sweetness: &[i64], k: i64) -> i64 {
    let mut lo = 1;
    let mut hi = sweetness.iter().sum::<i64>() / (k + 1);
    while lo < hi {
        let mid = (lo + hi + 1) / 2;
        if pieces(sweetness, mid) >= k + 1 {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1231;
    let mut bars: Vec<Vec<i64>> = Vec::new();
    let mut cuts: Vec<i64> = Vec::new();
    for _ in 0..100 {
        bars.push((0..10000).map(|_| next_random(&mut seed) % 100000 + 1).collect());
        cuts.push(next_random(&mut seed) % 10000);
    }
    let mut check = 0i64;
    for _ in 0..20 {
        for b in 0..100 {
            check = (check * 131 + maximize_sweetness(&bars[b], cuts[b])) % 1000000007;
        }
    }
    println!("100 bars of 10^4 chunks, 20 passes: checksum {}", check);
}
