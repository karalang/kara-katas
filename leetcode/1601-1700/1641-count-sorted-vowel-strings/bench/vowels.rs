// LeetCode #1641: Count Sorted Vowel Strings -- the bench's Rust mirror:
// the ★ arm on 4000000 random n from 1 to 50, all drawn first.

fn count_vowel_strings(n: i64) -> i64 {
    let mut ending = [1i64; 5];
    for _ in 1..n {
        for v in 1..5 {
            ending[v] += ending[v - 1];
        }
    }
    ending.iter().sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1641;
    let mut ns = Vec::new();
    for _ in 0..4000000 {
        ns.push(next_random(&mut seed) % 50 + 1);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &n in &ns {
        let count = count_vowel_strings(n);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    println!("4000000 random n: counts sum to {}, checksum {}", total, check);
}
