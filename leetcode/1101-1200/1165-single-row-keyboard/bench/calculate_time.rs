// LeetCode #1165: Single-Row Keyboard -- Rust mirror of the Kāra ★ arm: each
// letter's place in a table of 26, then the moves summed from place 0.

fn calculate_time(keyboard: &str, word: &str) -> i64 {
    let mut place = [0i64; 26];
    for (i, c) in keyboard.bytes().enumerate() {
        place[(c - b'a') as usize] = i as i64;
    }
    let mut at = 0;
    let mut time = 0;
    for c in word.bytes() {
        let next = place[(c - b'a') as usize];
        time += (next - at).abs();
        at = next;
    }
    time
}

fn main() {
    let mut seed: i64 = 1165;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut keyboards: Vec<String> = Vec::new();
    let mut words: Vec<String> = Vec::new();
    for _ in 0..16 {
        let mut b: Vec<u8> = (0..26).map(|i| b'a' + i as u8).collect();
        for i in (1..26).rev() {
            let j = (next_random() % (i as i64 + 1)) as usize;
            b.swap(i, j);
        }
        keyboards.push(String::from_utf8(b).unwrap());
        let w: Vec<u8> = (0..10000).map(|_| b'a' + (next_random() % 26) as u8).collect();
        words.push(String::from_utf8(w).unwrap());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..5000 {
        for k in 0..16 {
            let from = (next_random() % 5000) as usize;
            let t = calculate_time(&keyboards[k], &words[k][from..]);
            total += t;
            check = (check * 31 + t) % 1000000007;
        }
    }
    println!("5000 rounds over 16 words of 10^4 letters: total {}, checksum {}", total, check);
}
