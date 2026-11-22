// LeetCode #2719: Count of Integers -- the bench (integers.kara in Rust):
// the good numbers up to each bound by a digit-by-digit recursion, a free
// place's count remembered by place and digit sum.

const MOD: i64 = 1000000007;

fn good_up_to(bound: &str, min_sum: i64, max_sum: i64) -> i64 {
    let digits: Vec<i64> = bound.bytes().map(|b| (b - b'0') as i64).collect();
    let mut memo: Vec<Vec<i64>> = vec![vec![-1; (max_sum + 1) as usize]; digits.len()];
    walk(&digits, 0, 0, true, min_sum, max_sum, &mut memo)
}

fn walk(digits: &[i64], place: usize, sum: i64, tight: bool, min_sum: i64, max_sum: i64, memo: &mut Vec<Vec<i64>>) -> i64 {
    if sum > max_sum {
        return 0;
    }
    if place == digits.len() {
        return if sum >= min_sum { 1 } else { 0 };
    }
    if !tight && memo[place][sum as usize] >= 0 {
        return memo[place][sum as usize];
    }
    let top = if tight { digits[place] } else { 9 };
    let mut ways = 0;
    for d in 0..=top {
        ways = (ways + walk(digits, place + 1, sum + d, tight && d == top, min_sum, max_sum, memo)) % MOD;
    }
    if !tight {
        memo[place][sum as usize] = ways;
    }
    ways
}

fn count(num1: &str, num2: &str, min_sum: i64, max_sum: i64) -> i64 {
    let own: i64 = num1.bytes().map(|b| (b - b'0') as i64).sum();
    let itself = if min_sum <= own && own <= max_sum { 1 } else { 0 };
    (good_up_to(num2, min_sum, max_sum) - good_up_to(num1, min_sum, max_sum) + itself + MOD) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let ranges = 300;
    let rounds = 10;
    let mut seed: i64 = 2719;
    let mut problems: Vec<(String, String, i64, i64)> = Vec::new();
    for _ in 0..ranges {
        let mut num1 = String::new();
        let mut num2 = String::new();
        num1.push((b'1' + (next_random(&mut seed) % 4) as u8) as char);
        num2.push((b'5' + (next_random(&mut seed) % 5) as u8) as char);
        for _ in 1..22 {
            num1.push((b'0' + (next_random(&mut seed) % 10) as u8) as char);
            num2.push((b'0' + (next_random(&mut seed) % 10) as u8) as char);
        }
        let low = next_random(&mut seed) % 400 + 1;
        let high = low + next_random(&mut seed) % (401 - low);
        problems.push((num1, num2, low, high));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (num1, num2, low, high) in problems.iter() {
            let found = count(num1, num2, *low, *high);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{} ranges of 22 digits, {} rounds: counts mod p sum to {}, checksum {}", ranges, rounds, sum, check);
}
