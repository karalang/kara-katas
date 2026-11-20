// LeetCode #1268 bench, in Rust: the ★ arm (the products sorted, a binary
// search for each prefix typed, and up to three products from there that
// start with it) on 100 random lists of 1000 words of 1 to 10 letters from
// `a` to `d` built once, each searched for its own 20-letter word, 100
// rounds; every suggestion folded into a checksum.

fn suggested_products(products: &[String], search_word: &str) -> Vec<Vec<String>> {
    let mut sorted = products.to_vec();
    sorted.sort();
    let mut out = Vec::new();
    for end in 1..=search_word.len() {
        let prefix = &search_word[..end];
        let mut lo = 0;
        let mut hi = sorted.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if sorted[mid].as_str() < prefix {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        let mut list = Vec::new();
        let mut i = lo;
        while i < sorted.len() && list.len() < 3 && sorted[i].starts_with(prefix) {
            list.push(sorted[i].clone());
            i += 1;
        }
        out.push(list);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(longest: i64, seed: &mut i64) -> String {
    let len = next_random(seed) % longest + 1;
    (0..len).map(|_| (b'a' + (next_random(seed) % 4) as u8) as char).collect()
}

fn main() {
    let mut seed = 1268;
    let mut lists: Vec<Vec<String>> = Vec::new();
    let mut searches: Vec<String> = Vec::new();
    for _ in 0..100 {
        lists.push((0..1000).map(|_| random_word(10, &mut seed)).collect());
        searches.push((0..20).map(|_| (b'a' + (next_random(&mut seed) % 4) as u8) as char).collect());
    }
    let mut check: i64 = 0;
    for round in 0..100 {
        for l in 0..100 {
            for list in suggested_products(&lists[l], &searches[l]).iter() {
                check = (check * 131 + list.len() as i64 + round) % 1000000007;
                for w in list.iter() {
                    for b in w.bytes() {
                        check = (check * 131 + b as i64) % 1000000007;
                    }
                }
            }
        }
    }
    println!("100 rounds of 100 searches among 1000 words: checksum {}", check);
}
