// LeetCode #1137: N-th Tribonacci Number -- the bench, the ★ arm's algorithm:
// three running values.

fn tribonacci(n: i64) -> i64 {
    let mut a: i64 = 0;
    let mut b: i64 = 1;
    let mut c: i64 = 1;
    for _ in 0..n {
        let next = a + b + c;
        a = b;
        b = c;
        c = next;
    }
    a
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1137;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..20000000 {
        let n = next_random(&mut seed) % 38;
        let t = tribonacci(n);
        total += t;
        check = (check * 31 + t % 1000003) % 1000000007;
    }
    println!("20000000 queries, n from 0 to 37: answers total {}, checksum {}", total, check);
}
