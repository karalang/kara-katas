// LeetCode #1220 bench, Rust mirror of the Kāra ★ arm: five running counts,
// the strings of the length so far that end in each vowel, for every n from
// 1 to 8000; checksum of the answers.

fn count_vowel_permutation(n: i64) -> i64 {
    let modulus = 1_000_000_007;
    let (mut a, mut e, mut i, mut o, mut u) = (1i64, 1i64, 1i64, 1i64, 1i64);
    for _ in 1..n {
        (a, e, i, o, u) = ((e + i + u) % modulus, (a + i) % modulus, (e + o) % modulus, i, (i + o) % modulus);
    }
    (a + e + i + o + u) % modulus
}

fn main() {
    let mut check: i64 = 0;
    for n in 1..=8000 {
        check = (check * 131 + count_vowel_permutation(n)) % 1000000007;
    }
    println!("every n from 1 to 8000: checksum {}", check);
}
