// Benchmark for #522: Rust mirror of the ★ arm (longest first); see
// find_lus_length.kara.

fn is_subsequence(small: &str, big: &str) -> bool {
    let s: Vec<char> = small.chars().collect();
    let mut i = 0;
    for c in big.chars() {
        if i < s.len() && s[i] == c {
            i += 1;
        }
    }
    i == s.len()
}

fn find_lus_length(strs: &[String]) -> i64 {
    let mut order: Vec<usize> = (0..strs.len()).collect();
    order.sort_by(|&a, &b| strs[b].len().cmp(&strs[a].len()));
    for &i in order.iter() {
        let mut uncommon = true;
        for j in 0..strs.len() {
            if j != i && is_subsequence(&strs[i], &strs[j]) {
                uncommon = false;
                break;
            }
        }
        if uncommon {
            return strs[i].len() as i64;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut word = String::new();
    for _ in 0..len {
        word.push((97 + next_random(seed) % letters) as u8 as char);
    }
    word
}

fn main() {
    // 2,000 random lists of 50 words of 1 to 10 letters from 1 to 3
    // letters, one word in three a copy of an earlier one, made once;
    // then every list solved in each of 100 rounds.
    let mut seed: i64 = 522;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..2000 {
        let letters = 1 + next_random(&mut seed) % 3;
        let mut strs: Vec<String> = Vec::new();
        for k in 0..50i64 {
            if k > 0 && next_random(&mut seed) % 3 == 0 {
                let from = (next_random(&mut seed) % k) as usize;
                strs.push(strs[from].clone());
            } else {
                let len = 1 + next_random(&mut seed) % 10;
                strs.push(random_word(&mut seed, len, letters));
            }
        }
        lists.push(strs);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..100i64 {
        for (l, strs) in lists.iter().enumerate() {
            let answer = find_lus_length(strs);
            total += answer;
            checksum = (checksum + (round + 1) * (l as i64 + 1) * (answer + 2)) % 1000000007;
        }
    }
    println!("2000 lists of 50 words, 100 rounds: total {}, checksum {}", total, checksum);
}
