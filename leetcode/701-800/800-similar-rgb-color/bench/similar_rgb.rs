// LeetCode 800 — Similar RGB Color: the bench, in Rust. Mirrors
// similar_rgb.kara: each part rounded to the nearest doubled digit.

const DIGITS: &[u8] = b"0123456789abcdef";

fn digit(c: u8) -> i64 {
    if (48..=57).contains(&c) { c as i64 - 48 } else { c as i64 - 97 + 10 }
}

fn similar_rgb(color: &str) -> String {
    let b = color.as_bytes();
    let mut out = String::new();
    out.push('#');
    for p in 0..3 {
        let part = digit(b[1 + 2 * p]) * 16 + digit(b[2 + 2 * p]);
        let d = DIGITS[((part + 8) / 17) as usize] as char;
        out.push(d);
        out.push(d);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 800;
    let mut colors: Vec<String> = Vec::new();
    for _ in 0..4096 {
        let mut color = String::from("#");
        for _ in 0..6 {
            color.push(DIGITS[(next_random(&mut seed) % 16) as usize] as char);
        }
        colors.push(color);
    }
    let rounds: i64 = 40960000;
    let mut check = 0i64;
    for r in 0..rounds {
        let got = similar_rgb(&colors[(r % 4096) as usize]);
        let b = got.as_bytes();
        check = (check * 31 + b[1] as i64 * 65536 + b[3] as i64 * 256 + b[5] as i64) % 1000000007;
    }
    println!("{rounds} colours: checksum {check}");
}
