// Benchmark for #651: the best for every count of presses, as the Kara
// ★ arm.

fn max_a(n: i64) -> i64 {
    let mut best = vec![0i64; n as usize + 1];
    for i in 1..n as usize + 1 {
        best[i] = best[i - 1] + 1;
        for j in 1..i.saturating_sub(2) {
            best[i] = best[i].max(best[j] * (i - j - 1) as i64);
        }
    }
    best[n as usize]
}

fn main() {
    let calls: i64 = 200000;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for c in 0..calls {
        let a = max_a(1 + (c * 37) % 150);
        total = (total + a) % 1000000007;
        checksum = (checksum * 31 + a % 1000000007) % 1000000007;
    }
    println!("{calls} calls: total {total}, checksum {checksum}");
}
