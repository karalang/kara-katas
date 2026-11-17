// LeetCode #1186: Maximum Subarray Sum with One Deletion -- the ★ arm in
// Rust: one pass carrying the best sum ending here with nothing deleted
// (`kept`) and with one element deleted (`cut`).

fn maximum_sum(arr: &[i64]) -> i64 {
    let mut kept = arr[0];
    let mut cut = i64::MIN;
    let mut best = arr[0];
    for &x in arr[1..].iter() {
        cut = if cut == i64::MIN { kept } else { (cut + x).max(kept) };
        kept = (kept + x).max(x);
        best = best.max(kept).max(cut);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1182;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let arr: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 20001 - 10000).collect();
        arrays.push(arr);
    }
    let rounds = 100;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for arr in arrays.iter() {
            check = (check * 131 + maximum_sum(arr) + r) % 1000000007;
        }
    }
    println!("{rounds} rounds of 10 arrays: checksum {check}");
}
