// LeetCode #692: Top K Frequent Words -- bench program, Rust mirror of the select arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn top_k_frequent(words: &[String], k: usize) -> Vec<String> {
    let mut sorted = words.to_vec();
    sorted.sort();
    let mut distinct: Vec<String> = Vec::new();
    let mut counts: Vec<i64> = Vec::new();
    let mut i = 0;
    while i < sorted.len() {
        let mut j = i;
        while j < sorted.len() && sorted[j] == sorted[i] {
            j += 1;
        }
        distinct.push(sorted[i].clone());
        counts.push((j - i) as i64);
        i = j;
    }
    let mut out: Vec<String> = Vec::new();
    for _ in 0..k {
        let mut pick: i64 = -1;
        for d in 0..distinct.len() {
            if counts[d] > 0 && (pick < 0 || counts[d] > counts[pick as usize]) {
                pick = d as i64;
            }
        }
        out.push(distinct[pick as usize].clone());
        counts[pick as usize] = 0;
    }
    out
}

fn main() {
    let mut seed = 692;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..100 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..500 {
            let len = 1 + next_random(&mut seed) % 4;
            let mut w = String::new();
            for _ in 0..len {
                w.push((b'a' + (next_random(&mut seed) % 6) as u8) as char);
            }
            words.push(w);
        }
        lists.push(words);
    }
    let rounds = 60;
    let mut checksum: i64 = 0;
    let mut answers = 0;
    for _ in 0..rounds {
        for words in &lists {
            for w in top_k_frequent(words, 10) {
                for b in w.bytes() {
                    checksum = (checksum * 31 + b as i64) % 1000000007;
                }
                checksum = (checksum * 31 + 1) % 1000000007;
                answers += 1;
            }
        }
    }
    println!("{} rounds of 100 lists of 500 words: {} words answered, checksum {}", rounds, answers, checksum);
}
