// LeetCode #2847: Smallest Number With Given Digit Product -- the
// bench, mirrored from product.kara: the largest digit that divides
// what is left, 9 down to 2, and the digits smallest first.

fn smallest_number(n: i64) -> String {
    if n == 1 {
        return "1".to_string();
    }
    let mut rest = n;
    let mut digits: Vec<char> = Vec::new();
    for d in (2..10).rev() {
        while rest % d == 0 {
            digits.push(char::from_digit(d as u32, 10).unwrap());
            rest /= d;
        }
    }
    if rest != 1 {
        return "-1".to_string();
    }
    digits.iter().rev().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 20;
    let mut seed = 2847;
    let mut numbers: Vec<i64> = Vec::new();
    for _ in 0..count {
        let mut n: i64 = 1;
        for _ in 0..next_random(&mut seed) % 41 {
            let p = [2, 3, 5, 7][(next_random(&mut seed) % 4) as usize];
            if n <= 1000000000000000000 / p {
                n *= p;
            }
        }
        if next_random(&mut seed) % 10 == 0 && n <= 1000000000000000000 / 11 {
            n *= 11;
        }
        numbers.push(n);
    }
    let mut digits = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in numbers.iter() {
            let s = smallest_number(n);
            digits += s.len();
            for b in s.bytes() {
                check = (check * 31 + b as i64 + r) % 1000000007;
            }
        }
    }
    println!("{count} numbers, {rounds} rounds: {digits} digits, checksum {check}");
}
