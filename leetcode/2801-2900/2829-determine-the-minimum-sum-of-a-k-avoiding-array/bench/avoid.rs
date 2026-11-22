// LeetCode #2829: Determine the Minimum Sum of a k-avoiding Array -- the
// bench's Rust mirror of the ★ arm: the numbers walked up from 1, each
// taken unless its partner k - v was taken before it.

fn minimum_sum(n: i64, k: i64) -> i64 {
    let mut taken = vec![false; (n + k + 1) as usize];
    let mut count = 0;
    let mut sum = 0;
    let mut v = 1;
    while count < n {
        if v >= k || !taken[(k - v) as usize] {
            taken[v as usize] = true;
            count += 1;
            sum += v;
        }
        v += 1;
    }
    sum
}

fn main() {
    let rounds = 2000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for n in 1..=50 {
            for k in 1..=50 {
                let a = minimum_sum(n, k);
                total += a;
                check = (check * 31 + a + r) % 1000000007;
            }
        }
    }
    println!("2500 pairs, {} rounds: sums total {}, checksum {}", rounds, total, check);
}
