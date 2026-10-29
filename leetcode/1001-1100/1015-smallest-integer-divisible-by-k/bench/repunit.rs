// LeetCode #1015: Smallest Integer Divisible by K -- bench
// Mirrors repunit.kara; see ../README.md § Benchmarks.

fn smallest_repunit_div_by_k(k: i64) -> i64 {
    if k % 2 == 0 || k % 5 == 0 {
        return -1;
    }
    let mut r = 0;
    for length in 1..k + 1 {
        r = (r * 10 + 1) % k;
        if r == 0 {
            return length;
        }
    }
    -1
}

fn main() {
    let last: i64 = 30000;
    let mut none = 0;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for k in 1..last + 1 {
        let answer = smallest_repunit_div_by_k(k);
        if answer < 0 {
            none += 1;
        } else {
            total += answer;
        }
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("k = 1..{}: {} with no answer, the rest sum to {}, checksum {}", last, none, total, check);
}
