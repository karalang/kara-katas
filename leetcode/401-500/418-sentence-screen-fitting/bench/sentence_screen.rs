// LeetCode #418: Sentence Screen Fitting -- Rust mirror of
// sentence_screen.kara (one pointer into the text).

fn words_typing(sentence: &[String], rows: i64, cols: i64) -> i64 {
    let text = sentence.join(" ") + " ";
    let bytes = text.as_bytes();
    let length = text.len() as i64;
    let mut at: i64 = 0;
    for _ in 0..rows {
        at += cols;
        if bytes[(at % length) as usize] == b' ' {
            at += 1;
        } else {
            while at > 0 && bytes[((at - 1) % length) as usize] != b' ' {
                at -= 1;
            }
        }
    }
    at / length
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls = 10000;
    let mut seed: i64 = 418;
    let mut pool: Vec<String> = Vec::new();
    for _ in 0..200 {
        let length = 1 + step(&mut seed) % 10;
        let mut w = String::new();
        for _ in 0..length {
            w.push(char::from_u32((97 + step(&mut seed) % 26) as u32).unwrap());
        }
        pool.push(w);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let n = 1 + step(&mut seed) % 100;
        let mut sentence: Vec<String> = Vec::new();
        for _ in 0..n {
            sentence.push(pool[(step(&mut seed) % 200) as usize].clone());
        }
        let rows = 1 + step(&mut seed) % 20000;
        let cols = 10 + step(&mut seed) % 19991;
        let answer = words_typing(&sentence, rows, cols);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{calls} calls: total {total}, checksum {checksum}");
}
