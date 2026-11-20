// LeetCode #2376: Count Special Integers -- the bench, the ★ arm in Rust:
// the shorter numbers counted by length, then n's own length place by
// place, each place adding its smaller unused digits times the
// arrangements of the places after it.

fn arrangements(free: i64, places: i64) -> i64 {
    let mut ways = 1;
    for k in 0..places {
        ways *= free - k;
    }
    ways
}

fn count_special_numbers(n: i64) -> i64 {
    let digits: Vec<i64> = n.to_string().bytes().map(|b| (b - b'0') as i64).collect();
    let len = digits.len() as i64;
    let mut count = 0;
    for l in 1..len {
        count += 9 * arrangements(9, l - 1);
    }
    let mut used: Vec<bool> = vec![false; 10];
    for i in 0..len {
        let low = if i == 0 { 1 } else { 0 };
        let digit = digits[i as usize];
        for d in low..digit {
            if !used[d as usize] {
                count += arrangements(9 - i, len - 1 - i);
            }
        }
        if used[digit as usize] {
            return count;
        }
        used[digit as usize] = true;
    }
    count + 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10^5 values of 1 to 10 digits, at most 2 * 10^9
    let mut seed = 2376i64;
    let mut values: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let digits = 1 + next_random(&mut seed) % 10;
        let mut top = 1i64;
        for _ in 0..digits {
            top *= 10;
        }
        let high = next_random(&mut seed);
        let r = high * 32768 + next_random(&mut seed);
        values.push(1 + r % (top.min(2000000001) - 1));
    }
    let mut check = 0i64;
    for p in 0..100i64 {
        for &v in &values {
            check = (check * 31 + count_special_numbers(v) + p) % 1000000007;
        }
    }
    println!("100 passes over 10^5 values: checksum {}", check);
}
