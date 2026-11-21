// LeetCode #2514: Count Anagrams -- Rust mirror of the benchmark
// (anagrams.kara): the same sentences, passes, order and checksum.

const MOD: i64 = 1000000007;

fn power(base: i64, exponent: i64) -> i64 {
    let (mut result, mut b, mut e) = (1, base % MOD, exponent);
    while e > 0 {
        if e % 2 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e /= 2;
    }
    result
}

fn count_anagrams(s: &str) -> i64 {
    let mut factorial = vec![1i64; s.len() + 1];
    for i in 1..s.len() + 1 {
        factorial[i] = factorial[i - 1] * i as i64 % MOD;
    }
    let mut answer = 1;
    for word in s.split(' ') {
        let mut counts = vec![0usize; 26];
        for b in word.bytes() {
            counts[(b - b'a') as usize] += 1;
        }
        answer = answer * factorial[word.len()] % MOD;
        for &c in counts.iter() {
            answer = answer * power(factorial[c], MOD - 2) % MOD;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2514;
    let mut sentences: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut text = String::new();
        loop {
            let length = next_random(&mut seed) % 200 + 1;
            if text.len() as i64 + 1 + length > 100000 {
                break;
            }
            if !text.is_empty() {
                text.push(' ');
            }
            for _ in 0..length {
                text.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
            }
        }
        sentences.push(text);
    }
    let passes = 4;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 20;
        for k in 0..20 {
            check = (check * 31 + count_anagrams(&sentences[((start + k) % 20) as usize]) + p) % 1000000007;
        }
    }
    println!("{} passes over 20 sentences of 10^5: checksum {}", passes, check);
}
