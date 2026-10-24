// LeetCode #957: Prison Cells After N Days -- Rust mirror of the Kara
// bench program (a day per state seen).
use std::collections::HashMap;

fn next_day(cells: &[i64]) -> Vec<i64> {
    let mut out = vec![0i64; 8];
    for i in 1..7 {
        if cells[i - 1] == cells[i + 1] {
            out[i] = 1;
        }
    }
    out
}

fn code(cells: &[i64]) -> i64 {
    cells.iter().fold(0, |c, &v| c * 2 + v)
}

fn prison_after_n_days(cells: Vec<i64>, n: i64) -> Vec<i64> {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    let mut row = cells;
    let mut day = 0i64;
    let mut left = n;
    while left > 0 {
        if let Some(&first) = seen.get(&code(&row)) {
            left %= day - first;
            seen.clear();
            if left == 0 {
                break;
            }
        }
        seen.insert(code(&row), day);
        row = next_day(&row);
        day += 1;
        left -= 1;
    }
    row
}

fn main() {
    let rounds = 2000i64;
    let rows: Vec<Vec<i64>> = (0..256i64).map(|b| (0..8).map(|i| (b >> (7 - i)) & 1).collect()).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for b in 0..256 {
            let out = prison_after_n_days(rows[b].clone(), 1000000000 - r);
            let c = code(&out);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("{} rounds over all 256 rows: rows adding to {}, checksum {}", rounds, total, check);
}
