// Benchmark for #650: the sum of the prime factors, as the Kara ★ arm.

fn min_steps(n: i64) -> i64 {
    let mut rest = n;
    let mut steps = 0;
    let mut p = 2;
    while p * p <= rest {
        while rest % p == 0 {
            steps += p;
            rest /= p;
        }
        p += 1;
    }
    if rest > 1 {
        steps += rest;
    }
    steps
}

fn main() {
    let limit: i64 = 1000000;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for n in 1..limit + 1 {
        let steps = min_steps(n);
        total += steps;
        checksum = (checksum * 31 + steps) % 1000000007;
    }
    println!("1 to {limit}: total {total}, checksum {checksum}");
}
