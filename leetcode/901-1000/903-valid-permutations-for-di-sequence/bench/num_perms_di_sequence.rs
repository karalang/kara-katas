// LeetCode #903: Valid Permutations for DI Sequence -- bench program, Rust.
//
// Ranks of the last number with running sums, over one string of 4,000
// random letters built once. Each round counts its valid permutations,
// folds the count into a checksum and flips one letter.

fn num_perms_di_sequence(s: &str) -> i64 {
    let m: i64 = 1000000007;
    let letters = s.as_bytes();
    let n = letters.len();
    let mut ways: Vec<i64> = vec![1];
    for i in 1..n + 1 {
        let mut below: Vec<i64> = vec![0; i + 1];
        for k in 0..i {
            below[k + 1] = (below[k] + ways[k]) % m;
        }
        let mut next: Vec<i64> = vec![0; i + 1];
        for j in 0..i + 1 {
            next[j] = if letters[i - 1] == b'I' { below[j] } else { (below[i] - below[j] + m) % m };
        }
        ways = next;
    }
    let mut total = 0;
    for w in ways.iter() {
        total = (total + *w) % m;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let length: usize = 4000;
    let rounds: i64 = 12;
    let mut seed: i64 = 903;
    let mut letters: Vec<char> = Vec::new();
    for _ in 0..length {
        letters.push(if next_random(&mut seed) % 2 == 0 { 'D' } else { 'I' });
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        let s: String = letters.iter().collect();
        let got = num_perms_di_sequence(&s);
        check = (check * 31 + got) % 1000000007;
        let at = (r as usize * 7919) % length;
        letters[at] = if letters[at] == 'D' { 'I' } else { 'D' };
    }
    println!("{} rounds over {} letters: checksum {}", rounds, length, check);
}
