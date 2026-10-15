// Benchmark for #668: binary search on the value, counting by rows, as
// the Kara ★ arm.

fn find_kth_number(m: i64, n: i64, k: i64) -> i64 {
    let mut lo = 1;
    let mut hi = m * n;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        let mut count = 0;
        for i in 1..m + 1 {
            count += (mid / i).min(n);
        }
        if count >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    let rounds: i64 = 200;
    let mut sum: i64 = 0;
    for r in 0..rounds {
        let m = 30000 - r * 97 % 10000;
        let n = 30000 - r * 89 % 10000;
        let k = 1 + r * 7919813 % (m * n);
        sum = (sum * 31 + find_kth_number(m, n, k)) % 1000000007;
    }
    println!("{} rounds: checksum {}", rounds, sum);
}
