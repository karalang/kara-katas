// Benchmark workload — Sort Colors (LeetCode #75), seq lane.
// Rust single-threaded mirror of bench/sort_colors.kara. A batch of K=2000
// independent Dutch National Flag sorts of n=59999 {0,1,2} arrays (length not a
// multiple of 3, so the sorted result depends on the seed), each hashed, combined
// through a plain associative sum. This is the single-threaded baseline; the
// rayon variant (rayon/) is the hand-tuned parallel comparator for Kāra's
// auto-par. See ../README.md § Benchmarks.

fn sort_and_hash(seed: i64) -> i64 {
    let n: i64 = 59999;
    let mut a: Vec<i64> = Vec::new();
    for j in 0..n {
        a.push((j * 7 + seed) % 3);
    }

    let mut low: usize = 0;
    let mut mid: usize = 0;
    let mut high: i64 = n - 1;
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

    let mut acc: i64 = 0;
    for j in 0..n as usize {
        acc = (acc * 131 + a[j]) % 1_000_000_007;
    }
    acc
}

fn main() {
    const TOTAL: i64 = 2000;
    let mut sum: i64 = 0;
    for i in 0..TOTAL {
        sum += sort_and_hash(i);
    }
    println!("{}", sum);
}
