// LeetCode #2325: Decode the Message -- the bench, the ★ arm in Rust. One
// walk over the key's bytes fills a table of 26, each letter's first
// appearance given the next letter of the alphabet, and the message is
// read through it, spaces kept. O(|key| + |message|).

fn decode_message(key: &str, message: &str) -> String {
    let mut table = [0u8; 26];
    let mut next = b'a';
    for b in key.bytes() {
        if b != b' ' && table[(b - b'a') as usize] == 0 {
            table[(b - b'a') as usize] = next;
            next += 1;
        }
    }
    let mut decoded = String::new();
    for b in message.bytes() {
        decoded.push(if b == b' ' { ' ' } else { table[(b - b'a') as usize] as char });
    }
    decoded
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(seed: &mut i64) -> char {
    let roll = next_random(seed) % 27;
    if roll == 26 { ' ' } else { (b'a' + roll as u8) as char }
}

fn main() {
    let mut seed: i64 = 2325;
    let mut keys: Vec<String> = Vec::new();
    let mut messages: Vec<String> = Vec::new();
    for _ in 0..100 {
        let mut key = String::new();
        for _ in 0..1974 {
            key.push(letter(&mut seed));
        }
        key.push_str("abcdefghijklmnopqrstuvwxyz");
        keys.push(key);
        let mut message = String::new();
        for _ in 0..2000 {
            message.push(letter(&mut seed));
        }
        messages.push(message);
    }
    let mut check: i64 = 0;
    for p in 0..1000usize {
        for k in 0..100usize {
            let decoded = decode_message(&keys[k], &messages[k]);
            let bytes = decoded.as_bytes();
            check = (check * 31 + bytes[p % 2000] as i64 + bytes[(7 * p + k) % 2000] as i64) % 1000000007;
            let first = keys[k].chars().next().unwrap();
            keys[k] = format!("{}{}", &keys[k][1..], first);
        }
    }
    println!("1000 passes over 100 keys and messages of 2000: checksum {}", check);
}
