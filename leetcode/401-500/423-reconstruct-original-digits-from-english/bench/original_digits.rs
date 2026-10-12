// Benchmark for #423: mirror of original_digits.kara (unique letters).

fn original_digits(s: &str) -> String {
    let mut letters = [0i64; 26];
    for b in s.bytes() {
        letters[(b - b'a') as usize] += 1;
    }
    let at = |c: u8| letters[(c - b'a') as usize];
    let mut count = [0i64; 10];
    count[0] = at(b'z');
    count[2] = at(b'w');
    count[4] = at(b'u');
    count[6] = at(b'x');
    count[8] = at(b'g');
    count[3] = at(b'h') - count[8];
    count[5] = at(b'f') - count[4];
    count[7] = at(b's') - count[6];
    count[1] = at(b'o') - count[0] - count[2] - count[4];
    count[9] = at(b'i') - count[5] - count[6] - count[8];
    let mut out = String::new();
    for d in 0..10 {
        for _ in 0..count[d] {
            out.push((b'0' + d as u8) as char);
        }
    }
    out
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls: i64 = std::env::args().nth(1).map_or(100000, |s| s.parse().unwrap());
    let blocks: i64 = 20000;
    let names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
    let mut seed: i64 = 423;
    let mut text = String::new();
    let mut ends: Vec<usize> = vec![0];
    for _ in 0..blocks {
        let count = 1 + step(&mut seed) % 8;
        let mut pool: Vec<u8> = Vec::new();
        for _ in 0..count {
            pool.extend_from_slice(names[(step(&mut seed) % 10) as usize].as_bytes());
        }
        for i in 0..pool.len() {
            let j = i + (step(&mut seed) % (pool.len() - i) as i64) as usize;
            pool.swap(i, j);
        }
        for b in pool {
            text.push(b as char);
        }
        ends.push(text.len());
    }
    let mut digits: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let length = 50 + step(&mut seed) % 200;
        let first = (step(&mut seed) % (blocks - length)) as usize;
        let answer = original_digits(&text[ends[first]..ends[first + length as usize]]);
        digits += answer.len() as i64;
        for b in answer.bytes() {
            checksum = (checksum * 31 + (b as i64 - 47)) % 1000000007;
        }
    }
    println!("{calls} calls on {} letters: {digits} digits, checksum {checksum}", text.len());
}
