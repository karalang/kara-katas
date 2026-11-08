// LeetCode #1067: Digit Count in Range -- the benchmark's Rust mirror of
// digit_count.kara: the same place by place count over a million queries.

fn count_to(d: i64, n: i64) -> i64 {
    let mut total = 0;
    let mut p = 1;
    while p <= n {
        let above = n / (p * 10);
        let digit = n / p % 10;
        let below = n % p;
        if d == 0 {
            if above == 0 {
                break;
            }
            total += (above - 1) * p;
        } else {
            total += above * p;
        }
        if digit > d {
            total += p;
        } else if digit == d {
            total += below + 1;
        }
        p *= 10;
    }
    total
}

fn digits_count(d: i64, low: i64, high: i64) -> i64 {
    count_to(d, high) - count_to(d, low - 1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1067;
    let mut queries: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..1000000 {
        let d = next_random(&mut seed) % 10;
        let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 200000000 + 1;
        let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 200000000 + 1;
        queries.push((d, a.min(b), a.max(b)));
    }
    let mut calls = 0;
    let mut total = 0i64;
    let mut check = 0i64;
    for &(d, low, high) in queries.iter() {
        let answer = digits_count(d, low, high);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
        calls += 1;
    }
    println!("{calls} calls: answers sum {total}, checksum {check}");
}
