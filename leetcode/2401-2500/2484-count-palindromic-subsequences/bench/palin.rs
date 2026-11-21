// LeetCode #2484: Count Palindromic Subsequences -- bench, Rust mirror of
// palin.kara.

const MOD: i64 = 1000000007;

fn count_palindromes(s: &str) -> i64 {
    let digits: Vec<usize> = s.chars().map(|c| c as usize - '0' as usize).collect();
    let mut before_one = vec![0i64; 10];
    let mut before_two = vec![0i64; 100];
    let mut after_one = vec![0i64; 10];
    let mut after_two = vec![0i64; 100];
    for &d in digits.iter().rev() {
        for a in 0..10 {
            after_two[d * 10 + a] += after_one[a];
        }
        after_one[d] += 1;
    }
    let mut total = 0;
    for &d in &digits {
        after_one[d] -= 1;
        for a in 0..10 {
            after_two[d * 10 + a] -= after_one[a];
        }
        let mut here = 0;
        for a in 0..10 {
            for b in 0..10 {
                here += before_two[a * 10 + b] * after_two[b * 10 + a];
            }
        }
        total = (total + here) % MOD;
        for a in 0..10 {
            before_two[a * 10 + d] += before_one[a];
        }
        before_one[d] += 1;
    }
    total
}

fn main() {
    let mut seed: i64 = 2484;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut strings: Vec<Vec<i64>> = (0..4).map(|_| (0..2000).map(|_| next_random() % 10).collect()).collect();
    let mut check: i64 = 0;
    for p in 0..110 {
        for g in 0..4 {
            strings[g][(check % 2000) as usize] = check / 2000 % 10;
            let s: String = strings[g].iter().map(|d| d.to_string()).collect::<Vec<String>>().join("");
            check = (check * 31 + count_palindromes(&s) + p) % MOD;
        }
    }
    println!("110 passes over 4 strings of 2000 digits: checksum {}", check);
}
