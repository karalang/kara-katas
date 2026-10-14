// Benchmark for #567: Rust mirror of the ★ arm (a sliding window); see
// check_inclusion.kara.

fn check_inclusion(s1: &str, s2: &str) -> bool {
    let a: Vec<char> = s1.chars().collect();
    let b: Vec<char> = s2.chars().collect();
    let k = a.len();
    if k > b.len() {
        return false;
    }
    let mut need = vec![0i64; 26];
    for c in a.iter() {
        need[(*c as i64 - 'a' as i64) as usize] += 1;
    }
    let mut missing = k as i64;
    for i in 0..b.len() {
        let enter = (b[i] as i64 - 'a' as i64) as usize;
        if need[enter] > 0 {
            missing -= 1;
        }
        need[enter] -= 1;
        if i >= k {
            let leave = (b[i - k] as i64 - 'a' as i64) as usize;
            need[leave] += 1;
            if need[leave] > 0 {
                missing += 1;
            }
        }
        if missing == 0 {
            return true;
        }
    }
    false
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(length: i64, letters: i64, seed: &mut i64) -> String {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut s = String::new();
    for _ in 0..length {
        s.push(alphabet[(step(seed) % letters) as usize]);
    }
    s
}

fn main() {
    let count: i64 = 100;
    let rounds: i64 = 300;
    let mut seed: i64 = 567;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for g in 0..count {
        let letters = 3 + step(&mut seed) % 24;
        let len1 = 5 + step(&mut seed) % 196;
        let s1 = random_text(len1, letters, &mut seed);
        let mut s2 = random_text(10000, letters, &mut seed);
        if g % 2 == 0 {
            let mut shuffled: Vec<char> = s1.chars().collect();
            let mut i = shuffled.len() as i64 - 1;
            while i > 0 {
                let j = step(&mut seed) % (i + 1);
                shuffled.swap(i as usize, j as usize);
                i -= 1;
            }
            let cut = (step(&mut seed) % (10001 - s1.len() as i64)) as usize;
            let middle: String = shuffled.iter().collect();
            s2 = s2[..cut].to_string() + &middle + &s2[cut + s1.len()..];
        }
        pairs.push((s1, s2));
    }
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let (s1, s2) = &pairs[((round * 7 + g) % count) as usize];
            let got = check_inclusion(s1, s2);
            if got {
                found += 1;
            }
            checksum = (checksum * 31 + if got { g + 2 } else { 1 }) % 1000000007;
        }
    }
    println!("{} pairs, {} rounds: {} found, checksum {}", count, rounds, found, checksum);
}
