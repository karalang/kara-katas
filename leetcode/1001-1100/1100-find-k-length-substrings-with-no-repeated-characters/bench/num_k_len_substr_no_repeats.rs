// Benchmark: LeetCode #1100 Find K-Length Substrings With No Repeated
// Characters -- Rust mirror of num_k_len_substr_no_repeats.kara: the ★
// arm, a sliding window with a count of each letter, over 64 texts of
// 10^4 letters built once, 10 rounds each changing one letter per text and
// counting for 4 values of k.

fn num_k_len_substr_no_repeats(s: String, k: i64) -> i64 {
    let b = s.as_bytes();
    if k > 26 || k > b.len() as i64 {
        return 0;
    }
    let k = k as usize;
    let mut count = [0i64; 26];
    let mut repeated = 0;
    let mut found = 0;
    for i in 0..b.len() {
        let c = (b[i] - b'a') as usize;
        count[c] += 1;
        if count[c] == 2 {
            repeated += 1;
        }
        if i >= k {
            let out = (b[i - k] - b'a') as usize;
            count[out] -= 1;
            if count[out] == 1 {
                repeated -= 1;
            }
        }
        if i + 1 >= k && repeated == 0 {
            found += 1;
        }
    }
    found
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1100;
    let mut texts: Vec<Vec<char>> = Vec::new();
    for j in 0..64i64 {
        let alphabet = 8 + j % 19;
        texts.push((0..10000).map(|_| (b'a' + (next_random(&mut seed) % alphabet) as u8) as char).collect());
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10i64 {
        for j in 0..texts.len() {
            let at = ((round * 7919 + j as i64 * 104729) % 10000) as usize;
            texts[j][at] = (b'a' + ((round + j as i64) % 26) as u8) as char;
            let s: String = texts[j].iter().collect();
            for q in 0..4i64 {
                let k = (round * 7 + j as i64 * 3 + q * 11) % 30 + 1;
                let count = num_k_len_substr_no_repeats(s.clone(), k);
                total += count;
                check = (check * 31 + count + 1) % 1000000007;
            }
        }
    }
    println!("10 rounds over 64 texts of 10^4 letters: {} substrings, checksum {}", total, check);
}
