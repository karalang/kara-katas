// LeetCode #2438: Range Product Queries of Powers -- the bench, the ★ arm:
// the exponents' prefix sums, and two to each range's sum by squaring
// modulo 10^9 + 7.

const MOD: i64 = 1000000007;

fn power_of_two(exponent: i64) -> i64 {
    let mut result = 1;
    let mut base = 2;
    let mut e = exponent;
    while e > 0 {
        if e % 2 == 1 {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        e /= 2;
    }
    result
}

fn product_queries(n: i64, queries: &[Vec<i64>]) -> Vec<i64> {
    let mut prefix: Vec<i64> = vec![0];
    for bit in 0..31 {
        if (n >> bit) & 1 == 1 {
            let last = prefix[prefix.len() - 1];
            prefix.push(last + bit);
        }
    }
    let mut answers: Vec<i64> = Vec::new();
    for q in queries.iter() {
        answers.push(power_of_two(prefix[q[1] as usize + 1] - prefix[q[0] as usize]));
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2438;
    let mut values: Vec<i64> = Vec::new();
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..100 {
        let r = next_random(&mut seed);
        let n = 1 + (r * 32768 + next_random(&mut seed)) % 1000000000;
        let k = n.count_ones() as i64;
        let mut queries: Vec<Vec<i64>> = Vec::new();
        for _ in 0..10000 {
            let a = next_random(&mut seed) % k;
            let b = next_random(&mut seed) % k;
            queries.push(vec![a.min(b), a.max(b)]);
        }
        values.push(n);
        all.push(queries);
    }
    let mut check: i64 = 0;
    for p in 0..10usize {
        for c in 0..values.len() {
            let answers = product_queries(values[c], &all[c]);
            let m = answers.len();
            for i in 0..m {
                check = (check * 31 + answers[(i + p) % m] + p as i64) % 1000000007;
            }
        }
    }
    println!("10 passes over 100 values of 10^4 queries: checksum {}", check);
}
