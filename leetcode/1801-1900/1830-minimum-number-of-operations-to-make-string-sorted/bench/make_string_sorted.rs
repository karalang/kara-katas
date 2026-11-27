// LeetCode #1830: Minimum Number of Operations to Make String Sorted -- the
// bench in Rust: the ★ arm over 500 calls on runs of 1500 to 2999 letters cut
// from one string of 4500 random letters, built once, each run's start and
// length drawn from the checksum so far. Each call makes its run a string of
// its own.

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

fn make_string_sorted(s: String) -> i64 {
    let letters = s.as_bytes();
    let n = letters.len();
    let mut fact: Vec<i64> = vec![1; n + 1];
    for i in 1..n + 1 {
        fact[i] = fact[i - 1] * i as i64 % MOD;
    }
    let mut inverse: Vec<i64> = vec![1; n + 1];
    inverse[n] = power(fact[n], MOD - 2);
    for i in (0..n).rev() {
        inverse[i] = inverse[i + 1] * (i as i64 + 1) % MOD;
    }
    let mut count = [0usize; 26];
    let mut operations = 0;
    for i in (0..n).rev() {
        let c = (letters[i] - b'a') as usize;
        count[c] += 1;
        let smaller: usize = count[..c].iter().sum();
        let mut ways = fact[n - 1 - i] * smaller as i64 % MOD;
        for &k in count.iter() {
            ways = ways * inverse[k] % MOD;
        }
        operations = (operations + ways) % MOD;
    }
    operations
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1830;
    let letters: Vec<u8> = (0..4500).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
    let mut check: i64 = 0;
    for call in 0..500 {
        let start = ((check + call) % 1500) as usize;
        let len = (1500 + (check * 7 + call) % 1500) as usize;
        let s: String = letters[start..start + len].iter().map(|&b| b as char).collect();
        check = (check * 31 + make_string_sorted(s)) % 1000000007;
    }
    println!("500 calls: checksum {}", check);
}
