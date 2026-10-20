// LeetCode 808 — Soup Servings: the bench.
//
// Each round works out the answer for a size from 3750 to 4800 ml, 150
// to 192 servings, the largest the table is built for.
fn soup_servings(n: i64) -> f64 {
    if n > 4800 {
        return 1.0;
    }
    let m = ((n + 24) / 25) as usize;
    let mut p = vec![vec![0.0f64; m + 1]; m + 1];
    for a in 0..=m {
        for b in 0..=m {
            p[a][b] = if a == 0 && b == 0 {
                0.5
            } else if a == 0 {
                1.0
            } else if b == 0 {
                0.0
            } else {
                let mut sum = 0.0;
                for (da, db) in [(4, 0), (3, 1), (2, 2), (1, 3)] {
                    sum += p[a.saturating_sub(da)][b.saturating_sub(db)];
                }
                0.25 * sum
            };
        }
    }
    p[m][m]
}

fn main() {
    let rounds: i64 = 30000;
    let mut total = 0.0;
    let mut sure = 0;
    for r in 0..rounds {
        let n = 3750 + (r * 37) % 1051;
        let p = soup_servings(n);
        total += p;
        if p > 0.99999 {
            sure += 1;
        }
    }
    println!("{rounds} rounds of 3750 to 4800 ml: sum {total:.6}, {sure} above 0.99999");
}
