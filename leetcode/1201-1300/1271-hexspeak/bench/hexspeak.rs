// LeetCode #1271 bench, in Rust: the ★ arm (the decimal text parsed, its
// hexadecimal digits spelled from the lowest, 0 as O, 1 as I, 10 to 15 as A
// to F, any other an error) on 100,000 numbers up to 10^12 drawn once, half
// spelled in the eight letters, 150 rounds; every answer folded into a
// checksum.

fn to_hexspeak(num: &str) -> String {
    let mut n: i64 = num.parse().unwrap();
    let mut letters: Vec<char> = Vec::new();
    while n > 0 {
        let d = n % 16;
        if d == 0 {
            letters.push('O');
        } else if d == 1 {
            letters.push('I');
        } else if d >= 10 {
            letters.push((b'A' + (d - 10) as u8) as char);
        } else {
            return "ERROR".to_string();
        }
        n /= 16;
    }
    letters.iter().rev().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1271;
    let letters = [0i64, 1, 10, 11, 12, 13, 14, 15];
    let mut nums: Vec<String> = Vec::new();
    for i in 0..100000 {
        let n = if i % 2 == 0 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            (a * 32768 + b) % 1000000000000 + 1
        } else {
            let mut n = 1;
            for _ in 0..next_random(&mut seed) % 9 {
                n = n * 16 + letters[(next_random(&mut seed) % 8) as usize];
            }
            n
        };
        nums.push(n.to_string());
    }
    let mut check: i64 = 0;
    for round in 0..150 {
        for num in &nums {
            let s = to_hexspeak(num);
            check = (check * 131 + s.len() as i64 + round) % 1000000007;
            for b in s.bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("150 rounds of 100000 numbers: checksum {}", check);
}
