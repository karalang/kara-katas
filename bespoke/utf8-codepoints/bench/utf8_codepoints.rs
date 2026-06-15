// Rust mirror of the utf8-codepoints decode bench — same algorithm, same sink.
const MODULUS: i64 = 1000000007;
const REPEAT: i64 = 9523;
const ITERS: i64 = 400;

fn utf8_byte_len(lead: u8) -> i64 {
    if lead < 0x80 { 1 }
    else if (0xC0..=0xDF).contains(&lead) { 2 }
    else if (0xE0..=0xEF).contains(&lead) { 3 }
    else if (0xF0..=0xF7).contains(&lead) { 4 }
    else { 1 }
}

fn from_cps(cps: &[u32]) -> String {
    let mut s = String::new();
    for &cp in cps {
        if let Some(c) = char::from_u32(cp) { s.push(c); }
    }
    s
}

use std::hint::black_box;

fn main() {
    let base = from_cps(&[
        0x61, 0x62, 0x63, 0x20, 0x31, 0x32, 0x33, 0x20,
        0xe9, 0xf1, 0x3b1, 0x3b2, 0x434, 0x436,
        0x65e5, 0x672c, 0x1d11e, 0x1f980, 0x20,
    ]);
    let mut buf = String::new();
    for _ in 0..REPEAT { buf.push_str(&base); }
    let bytes = black_box(buf.as_bytes());
    let n = bytes.len() as i64;

    let mut sink: i64 = 0;
    let mut count: i64 = 0;
    for _ in 0..ITERS {
        let mut i: i64 = 0;
        while i < n {
            let lead = bytes[i as usize];
            let len = utf8_byte_len(lead);
            let mut cp: i64 = if len == 1 { lead as i64 }
                else if len == 2 { (lead & 0x1F) as i64 }
                else if len == 3 { (lead & 0x0F) as i64 }
                else { (lead & 0x07) as i64 };
            let mut k: i64 = 1;
            while k < len && i + k < n {
                let cont = bytes[(i + k) as usize];
                cp = (cp << 6) | ((cont & 0x3F) as i64);
                k += 1;
            }
            sink = (sink + cp) % MODULUS;
            count += 1;
            i += len;
        }
    }
    println!("{} {}", black_box(count), black_box(sink));
}
