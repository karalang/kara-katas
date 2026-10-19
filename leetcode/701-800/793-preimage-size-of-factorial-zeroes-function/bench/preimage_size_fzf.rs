// LeetCode 793 — Preimage Size of Factorial Zeroes Function: the bench,
// in Rust. Mirrors preimage_size_fzf.kara: binary search for the least x
// whose factorial has at least k zeroes at the end.

fn zeroes(x: i64) -> i64 {
    let mut count = 0;
    let mut p = x / 5;
    while p > 0 {
        count += p;
        p /= 5;
    }
    count
}

fn preimage_size_fzf(k: i64) -> i64 {
    let mut lo = 0;
    let mut hi = 5 * k + 5;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if zeroes(mid) < k {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if zeroes(lo) == k { 5 } else { 0 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 793;
    let rounds = 4000000;
    let mut fives = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let k = (a * 32768 + b) % 1000000001;
        let answer = preimage_size_fzf(k);
        if answer == 5 {
            fives += 1;
        }
        check = (check * 131 + k % 1000 + answer) % 1000000007;
    }
    println!("{rounds} values of k: {fives} with five, checksum {check}");
}
