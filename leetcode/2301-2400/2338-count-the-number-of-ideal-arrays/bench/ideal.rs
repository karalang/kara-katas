// LeetCode #2338: Count the Number of Ideal Arrays -- the bench, the ★ arm
// in Rust: the strictly increasing divisor chains of each length counted
// level by level, each length k + 1 spread over the n places in
// C(n - 1, k) ways.

const MODULUS: i64 = 1000000007;
const LONGEST: i64 = 14;

fn power(base: i64, exp: i64) -> i64 {
    let mut result = 1;
    let mut base = base % MODULUS;
    let mut exp = exp;
    while exp > 0 {
        if exp % 2 == 1 {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exp /= 2;
    }
    result
}

fn binomials(m: i64, count: i64) -> Vec<i64> {
    let mut out: Vec<i64> = vec![1];
    for k in 1..count {
        let next = out[(k - 1) as usize] * ((m - k + 1) % MODULUS) % MODULUS * power(k, MODULUS - 2) % MODULUS;
        out.push(next);
    }
    out
}

fn ideal_arrays(n: i64, max_value: i64) -> i64 {
    let ways = binomials(n - 1, LONGEST);
    let size = (max_value + 1) as usize;
    let mut ends: Vec<i64> = vec![1; size];
    ends[0] = 0;
    let mut answer = 0;
    for k in 0..LONGEST as usize {
        let mut total = 0;
        for v in 1..size {
            total = (total + ends[v]) % MODULUS;
        }
        answer = (answer + total * ways[k]) % MODULUS;
        let mut following: Vec<i64> = vec![0; size];
        for d in 1..size {
            if ends[d] != 0 {
                let mut m = 2 * d;
                while m < size {
                    following[m] = (following[m] + ends[d]) % MODULUS;
                    m += d;
                }
            }
        }
        ends = following;
    }
    answer
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let mut check = 0i64;
    for q in 0..300i64 {
        let n = 2 + scrambled(q + 1) % 9999;
        let max_value = 5000 + scrambled(q + 1001) % 5001;
        check = (check * 31 + ideal_arrays(n, max_value)) % 1000000007;
    }
    println!("300 queries of n up to 10^4 and maxValue 5000 to 10^4: checksum {}", check);
}
