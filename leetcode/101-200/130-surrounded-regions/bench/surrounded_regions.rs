// Benchmark harness for LeetCode #130 — Surrounded Regions.
// Mirrors surrounded_regions.kara algorithm-for-algorithm, including the
// nested Vec<Vec<i64>> board (not a flat array) and the explicit position
// stack.

fn flood(board: &mut [Vec<i64>], rows: i64, cols: i64, sr: i64, sc: i64) {
    let mut stack: Vec<i64> = Vec::new();
    stack.push(sr * cols + sc);
    while let Some(pos) = stack.pop() {
        let r = pos / cols;
        let c = pos % cols;
        if board[r as usize][c as usize] == 1 {
            board[r as usize][c as usize] = 2;
            if r + 1 < rows {
                stack.push((r + 1) * cols + c);
            }
            if r - 1 >= 0 {
                stack.push((r - 1) * cols + c);
            }
            if c + 1 < cols {
                stack.push(r * cols + (c + 1));
            }
            if c - 1 >= 0 {
                stack.push(r * cols + (c - 1));
            }
        }
    }
}

fn solve(board: &mut [Vec<i64>], rows: i64, cols: i64) {
    for r in 0..rows {
        for c in 0..cols {
            let on_border = r == 0 || r == rows - 1 || c == 0 || c == cols - 1;
            if on_border && board[r as usize][c as usize] == 1 {
                flood(board, rows, cols, r, c);
            }
        }
    }

    for r in 0..rows {
        for c in 0..cols {
            board[r as usize][c as usize] = if board[r as usize][c as usize] == 2 { 1 } else { 0 };
        }
    }
}

fn main() {
    let rows: i64 = 300;
    let cols: i64 = 300;
    let iters: i64 = 400;

    let mut pristine: Vec<Vec<i64>> = Vec::new();
    let mut x: i64 = 5;
    for _ in 0..rows {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..cols {
            x = (x * 1103515245 + 12345) % 2147483648;
            row.push((x / 65536) % 2);
        }
        pristine.push(row);
    }

    let mut sink: i64 = 0;
    for _ in 0..iters {
        let mut work: Vec<Vec<i64>> = Vec::new();
        for a in 0..rows {
            let mut row: Vec<i64> = Vec::new();
            for b in 0..cols {
                row.push(pristine[a as usize][b as usize]);
            }
            work.push(row);
        }

        solve(&mut work, rows, cols);

        let mut h: i64 = 0;
        for p in 0..rows {
            for q in 0..cols {
                h = (h * 31 + work[p as usize][q as usize]) % 1000000007;
            }
        }
        sink = (sink + h) % 1000000007;
    }
    println!("{}", sink);
}
