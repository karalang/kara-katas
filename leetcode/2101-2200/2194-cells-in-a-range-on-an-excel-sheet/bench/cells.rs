// benchmark's Rust mirror of cells.kara (LeetCode #2194, the ★ arm): two
// loops over the range's bytes.

fn cells_in_range(s: &str) -> Vec<String> {
    let b = s.as_bytes();
    let mut cells = Vec::new();
    for col in b[0]..=b[3] {
        for row in b[1]..=b[4] {
            cells.push(String::from_utf8(vec![col, row]).unwrap());
        }
    }
    cells
}

fn main() {
    let letters = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let mut ranges: Vec<String> = Vec::new();
    for c1 in 0..26 {
        for c2 in c1..26 {
            for r1 in 1..10 {
                for r2 in r1..10 {
                    ranges.push(format!("{}{}:{}{}", letters[c1] as char, r1, letters[c2] as char, r2));
                }
            }
        }
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        for s in &ranges {
            let cells = cells_in_range(s);
            let last = cells[cells.len() - 1].as_bytes();
            check = (check * 31 + cells.len() as i64 * 1000 + last[0] as i64 * 10 + last[1] as i64) % 1000000007;
        }
    }
    println!("20 passes over {} ranges: checksum {}", ranges.len(), check);
}
