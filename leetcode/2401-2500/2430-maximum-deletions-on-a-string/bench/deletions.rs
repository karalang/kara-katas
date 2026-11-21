// LeetCode #2430: Maximum Deletions on a String -- the bench, the ★ arm:
// the longest common prefix of the suffixes at `i` and `k` kept in two
// rows, each row from the one after it, and `best[i]` the most
// operations that clear the suffix from `i`.

fn delete_string(b: &[u8]) -> i64 {
    let n = b.len();
    let mut next_row: Vec<i64> = vec![0; n + 1];
    let mut row: Vec<i64> = vec![0; n + 1];
    let mut best: Vec<i64> = vec![0; n + 1];
    for i in (0..n).rev() {
        for k in i + 1..n {
            row[k] = if b[i] == b[k] { next_row[k + 1] + 1 } else { 0 };
        }
        best[i] = 1;
        for j in 1..(n - i) / 2 + 1 {
            if row[i + j] >= j as i64 {
                best[i] = best[i].max(best[i + j] + 1);
            }
        }
        std::mem::swap(&mut next_row, &mut row);
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2430;
    let mut words: Vec<Vec<u8>> = Vec::new();
    for _ in 0..8 {
        let mut w: Vec<u8> = Vec::new();
        for i in 0..4000usize {
            let back = 1 + next_random(&mut seed) % 3;
            if i as i64 >= back && next_random(&mut seed) % 2 == 0 {
                let c = w[i - back as usize];
                w.push(c);
            } else {
                w.push(b'a' + (next_random(&mut seed) % 2) as u8);
            }
        }
        words.push(w);
    }
    let mut check: i64 = 0;
    for p in 0..6i64 {
        for w in 0..words.len() {
            let at = ((p * 997 + w as i64 * 131) % 4000) as usize;
            words[w][at] = b'a' + (p % 2) as u8;
            check = (check * 31 + delete_string(&words[w]) + p) % 1000000007;
        }
    }
    println!("6 passes over 8 words of 4000 letters: checksum {}", check);
}
