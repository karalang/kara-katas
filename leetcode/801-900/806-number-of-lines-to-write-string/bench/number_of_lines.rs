// LeetCode 806 — Number of Lines To Write String: the bench.
//
// 64 strings of 1000 letters, LeetCode's longest, each with widths of
// its own from 2 to 10, are made once; each round counts the lines of
// the next one.
fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn number_of_lines(widths: &[i64], s: &str) -> (i64, i64) {
    let mut lines = 1;
    let mut width = 0;
    for b in s.bytes() {
        let w = widths[(b - 97) as usize];
        if width + w > 100 {
            lines += 1;
            width = w;
        } else {
            width += w;
        }
    }
    (lines, width)
}

fn main() {
    let mut seed = 806;
    let letters = b"abcdefghijklmnopqrstuvwxyz";
    let mut all_widths: Vec<Vec<i64>> = Vec::new();
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..64 {
        let widths: Vec<i64> = (0..26).map(|_| 2 + next_random(&mut seed) % 9).collect();
        all_widths.push(widths);
        let mut s = String::new();
        for _ in 0..1000 {
            s.push(letters[(next_random(&mut seed) % 26) as usize] as char);
        }
        strings.push(s);
    }
    let rounds: i64 = 1000000;
    let mut total = 0;
    let mut check = 0;
    for r in 0..rounds {
        let i = (r % 64) as usize;
        let (lines, width) = number_of_lines(&all_widths[i], &strings[i]);
        total += lines;
        check = (check * 131 + lines * 1000 + width) % 1000000007;
    }
    println!("{rounds} rounds of 1000 letters: {total} lines in all, checksum {check}");
}
