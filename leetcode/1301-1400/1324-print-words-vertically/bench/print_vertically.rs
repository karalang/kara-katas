// LeetCode #1324 bench, Rust mirror of the Kāra bench: the ★ arm (the words
// split apart, row i made of each word's i-th letter or a space, the row's
// end trimmed) on 100 sentences of 200 letters and spaces built once; then
// 1000 passes, each setting one letter of every sentence from the checksum
// so far, answering it and folding the rows' letters plus the pass into the
// checksum.

fn print_vertically(s: String) -> Vec<String> {
    let words: Vec<String> = s.split(' ').map(|w| w.to_string()).collect();
    let tallest = words.iter().map(|w| w.len()).max().unwrap();
    let mut rows: Vec<String> = Vec::new();
    for i in 0..tallest {
        let mut row = String::new();
        for w in words.iter() {
            row.push(if i < w.len() { w.as_bytes()[i] as char } else { ' ' });
        }
        rows.push(row.trim_end().to_string());
    }
    rows
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 200usize;
    let mut seed = 1324i64;
    let mut sentences: Vec<Vec<u8>> = Vec::new();
    for t in 0..100 {
        let longest = if t % 4 == 0 { 3 } else if t % 4 == 1 { 10 } else if t % 4 == 2 { 40 } else { 200 };
        let mut bytes: Vec<u8> = Vec::new();
        while bytes.len() < n {
            let len = 1 + next_random(&mut seed) % longest;
            for _ in 0..len {
                if bytes.len() < n {
                    bytes.push(b'A' + (next_random(&mut seed) % 26) as u8);
                }
            }
            if bytes.len() < n - 1 {
                bytes.push(b' ');
            }
        }
        sentences.push(bytes);
    }
    let mut check: i64 = 0;
    for pass in 0..1000i64 {
        for t in 0..100 {
            let bytes = &mut sentences[t];
            let at = (check % n as i64) as usize;
            if bytes[at] != b' ' {
                bytes[at] = b'A' + (check / 7 % 26) as u8;
            }
            let rows = print_vertically(String::from_utf8(bytes.clone()).unwrap());
            for row in rows.iter() {
                for b in row.bytes() {
                    check = (check * 131 + b as i64) % 1000000007;
                }
            }
            check = (check * 31 + rows.len() as i64 + pass) % 1000000007;
        }
    }
    println!("1000 passes over 100 sentences of 200: checksum {}", check);
}
