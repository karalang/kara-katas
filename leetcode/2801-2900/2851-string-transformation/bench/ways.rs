// LeetCode #2851: String Transformation -- the bench: the ★ arm over 10
// pairs of 5 * 10^5 letters, LeetCode's most, each s a block of up to 8
// letters repeated, half of them with one letter changed, t a rotation
// of s two times in three and otherwise s with one letter changed, k up
// to about 10^15, all drawn first, then each answered 5 times.

const MOD: i64 = 1000000007;

fn power(base: i64, exp: i64) -> i64 {
    let mut result = 1;
    let mut b = base % MOD;
    let mut e = exp;
    while e > 0 {
        if e % 2 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e /= 2;
    }
    result
}

fn number_of_ways(s: &str, t: &str, k: i64) -> i64 {
    let n = s.len();
    let text: Vec<u8> = s.bytes().chain(s.bytes()).collect();
    let pat: Vec<u8> = t.bytes().collect();
    let mut fail: Vec<usize> = vec![0; n];
    let mut j = 0;
    for i in 1..n {
        while j > 0 && pat[i] != pat[j] {
            j = fail[j - 1];
        }
        if pat[i] == pat[j] {
            j += 1;
        }
        fail[i] = j;
    }
    let mut at_zero = 0i64;
    let mut elsewhere = 0i64;
    j = 0;
    for i in 0..2 * n - 1 {
        while j > 0 && text[i] != pat[j] {
            j = fail[j - 1];
        }
        if text[i] == pat[j] {
            j += 1;
        }
        if j == n {
            if i + 1 == n {
                at_zero += 1;
            } else {
                elsewhere += 1;
            }
            j = fail[j - 1];
        }
    }
    let n = n as i64;
    let all = power(n - 1, k);
    let sign = if k % 2 == 0 { 1 } else { MOD - 1 };
    let inverse = power(n, MOD - 2);
    let zero_ways = (all + (n - 1) * sign) % MOD * inverse % MOD;
    let other_ways = (all - sign + MOD) % MOD * inverse % MOD;
    (at_zero * zero_ways + elsewhere * other_ways) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds = 5;
    let n: usize = 500000;
    let mut seed = 2851;
    let mut pairs: Vec<(String, String, i64)> = Vec::new();
    for _ in 0..count {
        let block = (next_random(&mut seed) % 8 + 1) as usize;
        let letters = next_random(&mut seed) % 3 + 1;
        let unit: Vec<u8> = (0..block).map(|_| b'a' + (next_random(&mut seed) % letters) as u8).collect();
        let mut s: Vec<u8> = (0..n).map(|i| unit[i % block]).collect();
        if next_random(&mut seed) % 2 == 0 {
            let at = (wide(&mut seed) % n as i64) as usize;
            s[at] = b'a' + (next_random(&mut seed) % 3) as u8;
        }
        let t: Vec<u8> = if next_random(&mut seed) % 3 < 2 {
            let r = (wide(&mut seed) % n as i64) as usize;
            s[n - r..].iter().chain(s[..n - r].iter()).copied().collect()
        } else {
            let mut t = s.clone();
            let at = (wide(&mut seed) % n as i64) as usize;
            t[at] = b'a' + (t[at] - b'a' + 1) % 3;
            t
        };
        let k = wide(&mut seed) * 900000 + 1;
        pairs.push((String::from_utf8(s).unwrap(), String::from_utf8(t).unwrap(), k));
    }
    let mut check = 0i64;
    for r in 0..rounds {
        for (s, t, k) in pairs.iter() {
            check = (check * 31 + number_of_ways(s, t, *k) + r) % MOD;
        }
    }
    println!("{count} pairs of {n}, {rounds} rounds: checksum {check}");
}
