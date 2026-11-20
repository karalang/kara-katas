// LeetCode #1239: the benchmark, mirroring the Kāra file.

fn mask_of(word: &str) -> Option<i64> {
    let mut mask: i64 = 0;
    for b in word.bytes() {
        let bit = 1i64 << (b - 97);
        if mask & bit != 0 {
            return None;
        }
        mask |= bit;
    }
    Some(mask)
}

fn search(masks: &[i64], at: usize, taken: i64) -> i64 {
    if at == masks.len() {
        return taken.count_ones() as i64;
    }
    let mut best = search(masks, at + 1, taken);
    if taken & masks[at] == 0 {
        best = best.max(search(masks, at + 1, taken | masks[at]));
    }
    best
}

fn max_length(arr: &[String]) -> i64 {
    let masks: Vec<i64> = arr.iter().filter_map(|w| mask_of(w)).collect();
    search(&masks, 0, 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1239;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..20000 {
        let mut words = Vec::new();
        for _ in 0..16 {
            let len = next_random(&mut seed) % 2 + 1;
            let mut w = String::new();
            for _ in 0..len {
                w.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
            }
            words.push(w);
        }
        lists.push(words);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for words in lists.iter() {
        let best = max_length(words);
        total += best;
        check = (check * 131 + best) % 1000000007;
    }
    println!("20000 lists of 16 words: total {}, checksum {}", total, check);
}
