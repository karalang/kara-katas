// Benchmark for #639: mirror of decode_ways_ii.kara (the ★ arm: the count
// of decodings of every prefix, two at a time) on the same workload.

const M: i64 = 1000000007;
const ROUNDS: usize = 600;

fn alone(c: u8) -> i64 {
    if c == b'*' {
        9
    } else if c == b'0' {
        0
    } else {
        1
    }
}

fn together(a: u8, b: u8) -> i64 {
    if a == b'*' {
        if b == b'*' {
            15
        } else if b <= b'6' {
            2
        } else {
            1
        }
    } else if a == b'1' {
        if b == b'*' { 9 } else { 1 }
    } else if a == b'2' {
        if b == b'*' {
            6
        } else if b <= b'6' {
            1
        } else {
            0
        }
    } else {
        0
    }
}

fn num_decodings(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let mut before = 1;
    let mut last = alone(bytes[0]);
    for i in 1..bytes.len() {
        let next = (last * alone(bytes[i]) + before * together(bytes[i - 1], bytes[i])) % M;
        before = last;
        last = next;
    }
    last
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 639;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut s = String::new();
        let mut prev = b'1';
        for _ in 0..100000 {
            let mut c = b'*';
            if next_random(&mut seed) % 10 >= 3 {
                c = b'1' + (next_random(&mut seed) % 9) as u8;
                if next_random(&mut seed) % 100 == 0 && (prev == b'1' || prev == b'2' || prev == b'*') {
                    c = b'0';
                }
            }
            s.push(c as char);
            prev = c;
        }
        texts.push(s);
    }
    let mut total = 0;
    let mut checksum = 0;
    for round in 0..ROUNDS {
        let count = num_decodings(&texts[round % 20]);
        total = (total + count) % M;
        checksum = (checksum * 31 + count) % M;
    }
    println!("20 strings of 100000 characters, {} rounds: total {}, checksum {}", ROUNDS, total, checksum);
}
