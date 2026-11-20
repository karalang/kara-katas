// LeetCode #1228 bench: the ★ arm in Rust, over the same 2000 random
// progressions and 2000 passes as the Kāra bench.

fn missing_number(arr: &[i64]) -> i64 {
    let n = arr.len() as i64;
    let step = (arr[arr.len() - 1] - arr[0]) / n;
    let mut lo = 0i64;
    let mut hi = n - 1;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if arr[mid as usize] == arr[0] + mid * step {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    arr[0] + lo * step
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1228;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let first = next_random(&mut seed) % 100001;
        let low = -(first / 1000);
        let high = (100000 - first) / 1000;
        let step = low + next_random(&mut seed) % (high - low + 1);
        let gone = next_random(&mut seed) % 999 + 1;
        arrays.push((0..1001).filter(|&i| i != gone).map(|i| first + i * step).collect());
    }
    let mut check: i64 = 0;
    for _ in 0..2000 {
        for arr in &arrays {
            check = (check * 131 + missing_number(arr)) % 1000000007;
        }
    }
    println!("2000 progressions of 1000 values, 2000 passes: checksum {check}");
}
