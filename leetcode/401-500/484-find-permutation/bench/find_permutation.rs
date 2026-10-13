// Benchmark for #484: Rust mirror of the ★ arm (1 to n, each run of Ds
// reversed); see find_permutation.kara.

fn find_permutation(s: &str) -> Vec<i64> {
    let letters: Vec<char> = s.chars().collect();
    let n = letters.len() + 1;
    let mut perm: Vec<i64> = (1..=n as i64).collect();
    let mut i = 0;
    while i < letters.len() {
        if letters[i] == 'D' {
            let start = i;
            while i < letters.len() && letters[i] == 'D' {
                i += 1;
            }
            let mut low = start;
            let mut high = i;
            while low < high {
                perm.swap(low, high);
                low += 1;
                high -= 1;
            }
        } else {
            i += 1;
        }
    }
    perm
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut patterns: Vec<String> = Vec::new();
    let mut seed: i64 = 484;
    for p in 0..20 {
        let mut s = String::new();
        for _ in 0..100000 {
            s.push(if next_random(&mut seed) % 20 < p { 'D' } else { 'I' });
        }
        patterns.push(s);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..10 {
        for s in &patterns {
            let perm = find_permutation(s);
            let n = perm.len();
            total += n as i64;
            checksum = (checksum * 31 + perm[0] + perm[n / 2] * 7 + perm[n - 1] * 13) % 1000000007;
        }
    }
    println!("200 solves of 100000 letters: {total} numbers, checksum {checksum}");
}
