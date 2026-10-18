// LeetCode #723: Candy Crush -- crushed cells marked by their sign.
// Benchmark mirror of the Kara star arm: each round marks every run of
// three across or down by negating its cells, then drops each column,
// until a round marks nothing; the board is crushed on a copy.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn candy_crush(board: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let mut b = board.to_vec();
    let m = b.len() as i64;
    let n = b[0].len() as i64;
    let mut stable = false;
    while !stable {
        stable = true;
        for r in 0..m as usize {
            for c in 0..(n - 2) as usize {
                let v = b[r][c].abs();
                if v != 0 && b[r][c + 1].abs() == v && b[r][c + 2].abs() == v {
                    b[r][c] = -v;
                    b[r][c + 1] = -v;
                    b[r][c + 2] = -v;
                    stable = false;
                }
            }
        }
        for r in 0..(m - 2) as usize {
            for c in 0..n as usize {
                let v = b[r][c].abs();
                if v != 0 && b[r + 1][c].abs() == v && b[r + 2][c].abs() == v {
                    b[r][c] = -v;
                    b[r + 1][c] = -v;
                    b[r + 2][c] = -v;
                    stable = false;
                }
            }
        }
        for c in 0..n as usize {
            let mut write = m - 1;
            let mut r = m - 1;
            while r >= 0 {
                if b[r as usize][c] > 0 {
                    b[write as usize][c] = b[r as usize][c];
                    write -= 1;
                }
                r -= 1;
            }
            while write >= 0 {
                b[write as usize][c] = 0;
                write -= 1;
            }
        }
    }
    b
}

fn main() {
    let mut seed: i64 = 723;
    let mut boards: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..40 {
        let mut board: Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..50 {
                row.push(1 + next_random(&mut seed) % 5);
            }
            board.push(row);
        }
        boards.push(board);
    }
    let mut sum = 0;
    for round in 0..100i64 {
        for d in 0..40i64 {
            let r = ((round * 7 + d) % 50) as usize;
            let c = ((round * 13 + d * 3) % 50) as usize;
            let du = d as usize;
            boards[du][r][c] = 1 + (boards[du][r][c] + round) % 5;
            let after = candy_crush(&boards[du]);
            for row in &after {
                for v in row {
                    if *v == 0 {
                        sum += 1;
                    }
                }
            }
        }
    }
    println!("100 rounds of 40 boards of 50 x 50: {} empty cells", sum);
}
