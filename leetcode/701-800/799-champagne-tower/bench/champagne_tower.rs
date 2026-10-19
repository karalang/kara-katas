// LeetCode 799 — Champagne Tower: the bench, in Rust. Mirrors
// champagne_tower.kara: one row at a time.

fn champagne_tower(poured: i64, query_row: i64, query_glass: i64) -> f64 {
    let mut row: Vec<f64> = vec![poured as f64];
    for r in 0..query_row as usize {
        let mut below: Vec<f64> = vec![0.0; r + 2];
        for c in 0..r + 1 {
            if row[c] > 1.0 {
                let half = (row[c] - 1.0) / 2.0;
                below[c] += half;
                below[c + 1] += half;
            }
        }
        row = below;
    }
    let got = row[query_glass as usize];
    if got > 1.0 { 1.0 } else { got }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 799;
    let mut questions: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..4096 {
        let hi = next_random(&mut seed);
        let poured = (hi * 32768 + next_random(&mut seed)) % 1000000001;
        let row = 50 + next_random(&mut seed) % 50;
        let glass = next_random(&mut seed) % (row + 1);
        questions.push((poured, row, glass));
    }
    let rounds: i64 = 81920;
    let mut total = 0.0f64;
    let mut check = 0i64;
    for r in 0..rounds {
        let (poured, row, glass) = questions[(r % 4096) as usize];
        let got = champagne_tower(poured, row, glass);
        total += got;
        check = (check * 31 + (got * 1000000.0) as i64) % 1000000007;
    }
    println!("{rounds} glasses: {total:.5} cups in all, checksum {check}");
}
