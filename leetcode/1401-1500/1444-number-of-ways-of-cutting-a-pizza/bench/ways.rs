// The Rust mirror of ways.kara: the same suffix sums and table, a fresh
// table for each count of pieces, as the Kara arm makes a fresh Vec.
fn ways(pizza: &[String], k: i32) -> i32 {
    let rows = pizza.len();
    let cols = pizza[0].len();
    let mut apples = vec![vec![0i64; cols + 1]; rows + 1];
    for r in (0..rows).rev() {
        let line = pizza[r].as_bytes();
        for c in (0..cols).rev() {
            let here = if line[c] == b'A' { 1 } else { 0 };
            apples[r][c] = here + apples[r + 1][c] + apples[r][c + 1] - apples[r + 1][c + 1];
        }
    }
    let mut ways = vec![vec![0i64; cols + 1]; rows + 1];
    for r in 0..rows {
        for c in 0..cols {
            if apples[r][c] > 0 {
                ways[r][c] = 1;
            }
        }
    }
    for _ in 1..k {
        let mut next = vec![vec![0i64; cols + 1]; rows + 1];
        for r in 0..rows {
            for c in 0..cols {
                let mut total = 0;
                for cut in r + 1..rows {
                    if apples[r][c] - apples[cut][c] > 0 {
                        total += ways[cut][c];
                    }
                }
                for cut in c + 1..cols {
                    if apples[r][c] - apples[r][cut] > 0 {
                        total += ways[r][cut];
                    }
                }
                next[r][c] = total % 1000000007;
            }
        }
        ways = next;
    }
    ways[0][0] as i32
}

fn main() {
    let mut seed: i64 = 1444;
    let mut check: i64 = 0;
    for _ in 0..200 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let rate = 5 + seed / 65536 % 46;
        let mut pizza: Vec<String> = Vec::new();
        for _ in 0..50 {
            let mut line = String::new();
            for _ in 0..50 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                line.push(if seed / 65536 % 100 < rate { 'A' } else { '.' });
            }
            pizza.push(line);
        }
        check = (check * 131 + ways(&pizza, 10) as i64) % 1000000007;
    }
    println!("200 pizzas of 50 by 50: checksum {}", check);
}
