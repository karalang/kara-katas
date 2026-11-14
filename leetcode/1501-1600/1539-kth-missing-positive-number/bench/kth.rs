// LeetCode #1539: Kth Missing Positive Number -- bench: the ★ arm (binary
// search on the count of missing numbers) over 1000 arrays of 1 to 1000
// values and 1000 values of k, built once, every pair asked 5 times. Rust
// mirror of kth.kara.

fn find_kth_positive(arr: &[i64], k: i64) -> i64 {
    let mut lo = 0usize;
    let mut hi = arr.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if arr[mid] - mid as i64 - 1 < k {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as i64 + k
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1539i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let n = next_random(&mut seed) % 1000 + 1;
        let gap = next_random(&mut seed) % 4 + 1;
        let mut arr = Vec::new();
        let mut value = 0i64;
        for _ in 0..n {
            value += next_random(&mut seed) % gap + 1;
            arr.push(value);
        }
        arrays.push(arr);
    }
    let mut ks = Vec::new();
    for _ in 0..1000 {
        ks.push(next_random(&mut seed) % 2000 + 1);
    }
    let mut check = 0i64;
    for _ in 0..5 {
        for arr in &arrays {
            for &k in &ks {
                check = mix(check, find_kth_positive(arr, k));
            }
        }
    }
    println!("5 passes over 1000 arrays of up to 1000 values and 1000 values of k: checksum {}", check);
}
