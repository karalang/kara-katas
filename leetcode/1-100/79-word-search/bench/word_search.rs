// Benchmark workload — Word Search (LeetCode #79).
// Rust mirror of bench/word_search.kara. Enumerates every self-avoiding walk (up to
// `depth` steps) from every start cell of a fixed all-'A' 5x5 board and folds each
// visited cell into a threaded accumulator — the 4-neighbour, in-place mark/restore
// DFS backtracking that powers word search, with the letter-match replaced by
// "any unvisited cell, up to depth" so every branch is taken. K=12 iterations seeded
// by the iteration index. The DFS recursion is the measured work. See ../README.md.

const ROWS: i64 = 5;
const COLS: i64 = 5;

// Nested heap board (Vec<Vec<u8>>) — the same pointer-chased, bounds-checked layout
// Kara's Vec[Vec[u8]] uses, so the comparison measures codegen on equal data
// structures rather than handing this mirror a fixed-stack-array advantage.
fn walk(board: &mut Vec<Vec<u8>>, r: i64, c: i64, depth: i64, acc: i64) -> i64 {
    if r < 0 || r >= ROWS || c < 0 || c >= COLS {
        return acc;
    }
    if board[r as usize][c as usize] == 0 {
        return acc;
    }
    let mut a = (acc * 131 + (r * COLS + c) + 1) % 1_000_000_007;
    if depth == 0 {
        return a;
    }
    let saved = board[r as usize][c as usize];
    board[r as usize][c as usize] = 0;
    a = walk(board, r + 1, c, depth - 1, a);
    a = walk(board, r - 1, c, depth - 1, a);
    a = walk(board, r, c + 1, depth - 1, a);
    a = walk(board, r, c - 1, depth - 1, a);
    board[r as usize][c as usize] = saved;
    a
}

fn search_all(board: &mut Vec<Vec<u8>>, depth: i64, seed: i64) -> i64 {
    let mut a = seed;
    for r in 0..ROWS {
        for c in 0..COLS {
            a = walk(board, r, c, depth, a);
        }
    }
    a
}

fn main() {
    const DEPTH: i64 = 25;
    const TOTAL: i64 = 12;
    const MODULUS: i64 = 1_000_000_007;

    let mut board: Vec<Vec<u8>> = vec![vec![b'A'; COLS as usize]; ROWS as usize];
    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let rr = search_all(&mut board, DEPTH, iter);
        sum = (sum + rr) % MODULUS;
    }
    println!("{}", sum);
}
