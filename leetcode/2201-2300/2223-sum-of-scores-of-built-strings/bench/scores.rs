// LeetCode #2223: Sum of Scores of Built Strings -- bench mirror of
// scores.kara: the Z-function by the Z-algorithm, z[0] = n, summed.

fn sum_scores(s: &str) -> i64 {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    let mut z: Vec<usize> = vec![0; n];
    z[0] = n;
    let (mut l, mut r) = (0usize, 0usize);
    for i in 1..n {
        if i < r {
            z[i] = (r - i).min(z[i - l]);
        }
        while i + z[i] < n && chars[z[i]] == chars[i + z[i]] {
            z[i] += 1;
        }
        if i + z[i] > r {
            l = i;
            r = i + z[i];
        }
    }
    z.iter().map(|&x| x as i64).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(seed: &mut i64) -> char {
    if next_random(seed) % 2 == 1 { 'b' } else { 'a' }
}

fn main() {
    let mut seed = 2223;
    let mut words: Vec<Vec<char>> = Vec::new();
    for _ in 0..20 {
        // 10^5 letters, each 'a' or 'b'
        words.push((0..100000).map(|_| letter(&mut seed)).collect());
    }
    let mut check: i64 = 0;
    for a in 0..20 {
        for r in 0..5 {
            // punch: one letter is drawn again before each answer
            words[a][r * 19999] = letter(&mut seed);
            let s: String = words[a].iter().collect();
            check = (check * 31 + sum_scores(&s)) % 1000000007;
        }
    }
    println!("20 strings of 10^5, 5 punches: checksum {check}");
}
