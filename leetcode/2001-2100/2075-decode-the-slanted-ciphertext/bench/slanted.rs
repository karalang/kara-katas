// LeetCode #2075: Decode the Slanted Ciphertext -- Rust mirror of the ★
// arm's benchmark (slanted.kara): 40 grids of 10^6 characters in 1 to 1000
// rows, built once and decoded.

fn decode_ciphertext(encoded_text: &str, rows: usize) -> String {
    let text = encoded_text.as_bytes();
    let cols = text.len() / rows;
    let mut plain = String::new();
    for c in 0..cols {
        let mut r = 0;
        while r < rows && c + r < cols {
            plain.push(text[r * cols + c + r] as char);
            r += 1;
        }
    }
    plain.trim_end().to_string()
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz      ".chars().collect();
    let mut seed: i64 = 2075;
    let mut grids: Vec<(String, usize)> = Vec::new();
    for g in 0..40 {
        let rows = [1, 2, 10, 100, 1000][g % 5];
        let mut text = String::new();
        for _ in 0..1000000 / rows * rows {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            text.push(letters[((seed / 65536) % 32) as usize]);
        }
        grids.push((text, rows));
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for (text, rows) in &grids {
        let plain = decode_ciphertext(text, *rows);
        total += plain.len();
        for &b in plain.as_bytes() {
            check = (check * 31 + b as i64) % 1000000007;
        }
    }
    println!("40 grids: {total} characters, checksum {check}");
}
