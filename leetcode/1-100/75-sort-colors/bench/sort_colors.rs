// Benchmark workload — Sort Colors (LeetCode #75).
// Rust mirror of bench/sort_colors.kara. Dutch National Flag one-pass sort over a
// Vec<i64> allocated ONCE (n=500) and reused: each of K=200_000 iterations refills
// it in place with a k-dependent {0,1,2} pattern, sorts in place, and folds the
// result into a rolling polynomial hash. The measured work is the sort's
// data-dependent branches and swaps, not allocation. See ../README.md § Benchmarks.

fn sort_colors(a: &mut Vec<i64>) {
    let n = a.len();
    if n == 0 {
        return;
    }
    let mut low: usize = 0;
    let mut mid: usize = 0;
    let mut high: i64 = n as i64 - 1;
    while mid as i64 <= high {
        if a[mid] == 0 {
            a.swap(low, mid);
            low += 1;
            mid += 1;
        } else if a[mid] == 1 {
            mid += 1;
        } else {
            a.swap(mid, high as usize);
            high -= 1;
        }
    }
}

fn main() {
    const N: i64 = 500;
    const TOTAL: i64 = 200_000;
    const MODULUS: i64 = 1_000_000_007;

    let mut a: Vec<i64> = vec![0; N as usize];

    let mut acc: i64 = 0;
    for k in 0..TOTAL {
        for j in 0..N {
            a[j as usize] = (j * 7 + k * 13) % 3;
        }
        sort_colors(&mut a);
        for j in 0..N as usize {
            acc = (acc * 131 + a[j]) % MODULUS;
        }
    }
    println!("{}", acc);
}
