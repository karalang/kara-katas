// LeetCode #1716: Calculate Money in Leetcode Bank -- the Rust mirror of
// the bench (money.kara): whole weeks and the days left in closed form, on
// 500000 random n, each answered 20 times.

fn total_money(n: i32) -> i32 {
    let weeks = n / 7;
    let days = n % 7;
    28 * weeks + 7 * weeks * (weeks - 1) / 2 + days * (weeks + 1) + days * (days - 1) / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 500000;
    let rounds: i64 = 20;
    let mut seed: i64 = 1716;
    let ns: Vec<i32> = (0..count).map(|_| (next_random(&mut seed) % 1000 + 1) as i32).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in ns.iter() {
            let answer = total_money(n) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} values of n, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
