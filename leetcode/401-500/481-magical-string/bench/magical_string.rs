// Benchmark for #481: Rust mirror of the ★ arm (the string read while it
// is written); see magical_string.kara.

fn magical_string(n: i64) -> i64 {
    let mut s: Vec<i64> = vec![1, 2, 2];
    let mut read = 2;
    while (s.len() as i64) < n {
        let next = 3 - s[s.len() - 1];
        for _ in 0..s[read] {
            s.push(next);
        }
        read += 1;
    }
    let mut ones = 0;
    for i in 0..n as usize {
        if s[i] == 1 {
            ones += 1;
        }
    }
    ones
}

fn main() {
    let rounds = 1000;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let ones = magical_string(100000 - r);
        total += ones;
        checksum = (checksum * 31 + ones) % 1000000007;
    }
    println!("{rounds} rounds of n = 99001 to 100000: 1s add up to {total}, checksum {checksum}");
}
