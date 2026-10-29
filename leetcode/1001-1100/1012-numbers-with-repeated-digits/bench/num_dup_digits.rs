// LeetCode #1012 bench: the ★ arm (counting arrangements) over 100,000
// values of n up to a billion, drawn once; each of 40 rounds counts every
// value shifted by its own amount and folds each count into a checksum.

fn num_dup_digits_at_most_n(n: i64) -> i64 {
    n - distinct_up_to(n)
}

fn distinct_up_to(n: i64) -> i64 {
    let mut digits: Vec<i64> = Vec::new();
    let mut rest = n;
    while rest > 0 {
        digits.push(rest % 10);
        rest /= 10;
    }
    digits.reverse();
    let len = digits.len() as i64;
    let mut count = 0;
    for k in 1..len {
        count += 9 * arrangements(9, k - 1);
    }
    let mut seen = vec![false; 10];
    for i in 0..len {
        let d = digits[i as usize];
        let lowest = if i == 0 { 1 } else { 0 };
        for smaller in lowest..d {
            if !seen[smaller as usize] {
                count += arrangements(9 - i, len - i - 1);
            }
        }
        if seen[d as usize] {
            return count;
        }
        seen[d as usize] = true;
    }
    count + 1
}

fn arrangements(free: i64, slots: i64) -> i64 {
    let mut ways = 1;
    for j in 0..slots {
        ways *= free - j;
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 40;
    let mut seed = 1012;
    let mut values: Vec<i64> = Vec::new();
    for _ in 0..count {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        values.push((hi * 32768 + lo) % 1000000000);
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        for k in 0..count {
            let n = (values[k] + r as i64 * 7919) % 1000000000 + 1;
            check = (check * 31 + num_dup_digits_at_most_n(n)) % 1000000007;
        }
    }
    println!("{} rounds over {} values of n: checksum {}", rounds, count, check);
}
