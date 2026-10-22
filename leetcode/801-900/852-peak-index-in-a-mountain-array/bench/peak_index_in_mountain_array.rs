// Benchmark for #852: Peak Index in a Mountain Array -- Rust twin of the
// Kāra ★ arm (binary search on the slope).

fn peak_index_in_mountain_array(arr: &[i64]) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = arr.len() - 1;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if arr[mid] < arr[mid + 1] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 64;
    let rounds = 30000000;
    let n: i64 = 100000;
    let mut seed: i64 = 852;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let step = 1 + (g % 10) as i64;
        let peak = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 2);
        let mut arr: Vec<i64> = Vec::new();
        let mut v: i64 = 0;
        let mut low: i64 = 0;
        for i in 0..n {
            if i > 0 {
                if i <= peak {
                    v += 1 + next_random(&mut seed) % step;
                } else {
                    v -= 1 + next_random(&mut seed) % step;
                }
            }
            arr.push(v);
            low = low.min(v);
        }
        for x in arr.iter_mut() {
            *x -= low;
        }
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let p = peak_index_in_mountain_array(&arrays[round % count]);
        total += p;
        checksum = (checksum * 31 + p) % 1000000007;
    }
    println!("{} rounds of {} mountains: peaks sum to {}, checksum {}", rounds, count, total, checksum);
}
