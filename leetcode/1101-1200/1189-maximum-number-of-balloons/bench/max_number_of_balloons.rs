// LeetCode #1189 bench: the ★ arm in Rust, over the same 200 texts of 10^4
// letters and 200 rounds as the Kāra bench.

fn max_number_of_balloons(text: &str) -> i64 {
    let mut count = [0i64; 26];
    for b in text.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    let letter = |c: u8| count[(c - b'a') as usize];
    *[letter(b'b'), letter(b'a'), letter(b'l') / 2, letter(b'o') / 2, letter(b'n')]
        .iter()
        .min()
        .unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(seed: &mut i64, n: usize, letters: &str) -> String {
    let pool: Vec<char> = letters.chars().collect();
    let mut s = String::with_capacity(n);
    for _ in 0..n {
        s.push(pool[(next_random(seed) % pool.len() as i64) as usize]);
    }
    s
}

fn main() {
    let alphabets = ["abcdefghijklmnopqrstuvwxyz", "balloon", "balonxy"];
    let mut seed = 1189;
    let texts: Vec<String> = (0..200)
        .map(|i| random_text(&mut seed, 10000, alphabets[i % 3]))
        .collect();
    let mut check: i64 = 0;
    for _ in 0..ROUNDS {
        for t in &texts {
            check = (check * 131 + max_number_of_balloons(t) + 1) % 1000000007;
        }
    }
    println!("{ROUNDS} rounds of 200 texts of 10000 letters: checksum {check}");
}

const ROUNDS: usize = 200;
