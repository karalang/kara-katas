// Benchmark twin for LeetCode #289 — same algorithm as gameoflife.kara.
//
// Two-bit in-place encoding: bit 0 old generation, bit 1 new. `& 1` on every
// neighbour read keeps the sweep order irrelevant.

const ROWS: usize = 256;
const COLS: usize = 256;
const GENS: usize = 60;

fn next_rand(s: i64) -> i64 { (s.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647 }

fn live_neighbours(board: &[[i64; COLS]; ROWS], r: usize, c: usize) -> i64 {
    let mut n = 0i64;
    for dr in -1i64..=1 {
        for dc in -1i64..=1 {
            if dr == 0 && dc == 0 { continue; }
            let rr = r as i64 + dr;
            let cc = c as i64 + dc;
            if rr >= 0 && rr < ROWS as i64 && cc >= 0 && cc < COLS as i64 {
                n += board[rr as usize][cc as usize] & 1;
            }
        }
    }
    n
}

fn step(board: &mut [[i64; COLS]; ROWS]) {
    for r in 0..ROWS {
        for c in 0..COLS {
            let n = live_neighbours(board, r, c);
            let alive = (board[r][c] & 1) == 1;
            let lives = if alive { n == 2 || n == 3 } else { n == 3 };
            if lives { board[r][c] |= 2; }
        }
    }
    for r in 0..ROWS {
        for c in 0..COLS { board[r][c] >>= 1; }
    }
}

fn main() {
    let mut board = [[0i64; COLS]; ROWS];
    let mut seed = 20260820i64;
    for r in 0..ROWS {
        for c in 0..COLS {
            seed = next_rand(seed);
            board[r][c] = if ((seed / 65536) % 100) < 35 { 1 } else { 0 };
        }
    }
    for _ in 0..GENS { step(&mut board); }

    let mut pop = 0i64;
    let mut hash = 0i64;
    for r in 0..ROWS {
        for c in 0..COLS {
            if board[r][c] == 1 {
                pop += 1;
                hash = (hash * 31 + (r as i64 * COLS as i64 + c as i64)) % 1000000007;
            }
        }
    }
    println!("pop {} hash {}", pop, hash);
}
