// LeetCode #2288: Apply Discount to Prices -- the bench, the ★ arm in
// Rust. Split on spaces; a `$` and then only digits is a price,
// discounted in whole cents and written back with two decimals.

fn is_price(word: &str) -> bool {
    word.len() > 1 && word.starts_with('$') && word.bytes().skip(1).all(|b| b.is_ascii_digit())
}

fn discount_prices(sentence: &str, discount: i64) -> String {
    let mut words: Vec<String> = Vec::new();
    for word in sentence.split(' ') {
        if is_price(word) {
            let price: i64 = word[1..].parse().unwrap();
            let cents = price * (100 - discount);
            words.push(format!("${}.{:02}", cents / 100, cents % 100));
        } else {
            words.push(word.to_string());
        }
    }
    words.join(" ")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64) -> String {
    let kind = next_random(seed) % 4;
    let len = next_random(seed) % 8 + 1;
    let mut w = String::new();
    if kind < 2 {
        w.push('$');
    }
    for _ in 0..len {
        let r = next_random(seed);
        w.push(if kind == 0 || kind == 3 { (b'0' + (r % 10) as u8) as char } else { (b'a' + (r % 26) as u8) as char });
    }
    w
}

fn main() {
    let mut seed = 2288;
    let mut sentences: Vec<String> = Vec::new();
    for _ in 0..4000 {
        let words: Vec<String> = (0..12).map(|_| word(&mut seed)).collect();
        sentences.push(words.join(" "));
    }
    let mut check: i64 = 0;
    for pass in 0..50 {
        for sentence in &sentences {
            let answer = discount_prices(sentence, pass * 2);
            check = (check * 31 + answer.len() as i64 + answer.as_bytes()[answer.len() - 2] as i64) % 1000000007;
        }
    }
    println!("50 passes over 4000 sentences: checksum {}", check);
}
