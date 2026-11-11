// LeetCode #2114: Maximum Number of Words Found in Sentences -- the
// benchmark, the same algorithm as words.kara: each sentence's spaces
// counted over its bytes, plus one, and the largest taken.

fn most_words_found(sentences: &[String]) -> i64 {
    let mut most = 0i64;
    for s in sentences {
        let words = s.bytes().filter(|&b| b == b' ').count() as i64 + 1;
        most = most.max(words);
    }
    most
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2114i64;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..200 {
        let mut sentences: Vec<String> = Vec::new();
        for _ in 0..100 {
            let words = next_random(&mut seed) % 25 + 1;
            let mut s = String::new();
            for w in 0..words {
                if w > 0 {
                    s.push(' ');
                }
                for _ in 0..next_random(&mut seed) % 6 + 1 {
                    s.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
                }
            }
            sentences.push(s);
        }
        lists.push(sentences);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10usize {
        for a in 0..200usize {
            lists[a][(round * 37 + a) % 100].push_str(" a");
            let got = most_words_found(&lists[a]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("2000 solves: {} words, checksum {}", total, check);
}
