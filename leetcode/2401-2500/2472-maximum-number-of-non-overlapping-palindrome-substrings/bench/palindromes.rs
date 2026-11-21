// LeetCode #2472: Maximum Number of Non-overlapping Palindrome Substrings
// -- the bench, the ★ arm in Rust: the greedy over starts, a palindrome
// of `k` letters from here taken first, else one of `k + 1`, each checked
// by two indices walked inward. The strings are `Vec<char>`.

fn is_palindrome(c: &[char], mut lo: usize, mut hi: usize) -> bool {
    while lo < hi {
        if c[lo] != c[hi] {
            return false;
        }
        lo += 1;
        hi -= 1;
    }
    true
}

fn max_palindromes(c: &[char], k: usize) -> i64 {
    let n = c.len();
    let mut count = 0;
    let mut i = 0;
    while i + k <= n {
        if is_palindrome(c, i, i + k - 1) {
            count += 1;
            i += k;
        } else if i + k < n && is_palindrome(c, i, i + k) {
            count += 1;
            i += k + 1;
        } else {
            i += 1;
        }
    }
    count
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 strings of 2000 letters from "ab" built once; then 2400 passes,
    // each setting one letter of every string from the checksum so far,
    // then answering it with `k` from 2 to 6 by the pass, folding the
    // count plus the pass into the checksum
    let n = 2000usize;
    let letters = ['a', 'b'];
    let mut seed = 2472;
    let mut texts: Vec<Vec<char>> =
        (0..20).map(|_| (0..n).map(|_| letters[(next_random(&mut seed) % 2) as usize]).collect()).collect();
    let mut check = 0i64;
    for p in 0..2400i64 {
        let k = (2 + p % 5) as usize;
        for a in 0..texts.len() {
            texts[a][(check as usize + a) % n] = letters[(check % 2) as usize];
            check = (check * 31 + max_palindromes(&texts[a], k) + p) % 1000000007;
        }
    }
    println!("2400 passes over 20 strings of 2000: checksum {check}");
}
