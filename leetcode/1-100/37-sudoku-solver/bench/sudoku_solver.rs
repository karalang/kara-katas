// LeetCode #37 bench — Rust (mirror of sudoku_solver.kara).
//
// Bitmask backtracking solver over a flat [i64; 81] board with three stack [i64; 9]
// mask arrays, linear cell order, ascending digit order, XOR undo. Workload: TOTAL
// times copy the "world's hardest sudoku" template, clear cell k%81, solve in place,
// fold a position-weighted signature of the solved grid into a checksum. `rustc -O`
// wraps on overflow; the bench also builds a `-C overflow-checks=on` variant to match
// Kāra's checked-by-default semantics (all values stay well inside i64, so neither
// variant traps — the safety tax isolates codegen).

fn box_index(r: i64, c: i64) -> i64 {
    (r / 3) * 3 + c / 3
}

fn go(board: &mut [i64], rows: &mut [i64], cols: &mut [i64], boxes: &mut [i64], pos: i64) -> bool {
    if pos == 81 {
        return true;
    }
    let r = pos / 9;
    let c = pos % 9;
    if board[pos as usize] != 0 {
        return go(board, rows, cols, boxes, pos + 1);
    }
    let b = box_index(r, c);
    let used = rows[r as usize] | cols[c as usize] | boxes[b as usize];
    let mut d = 1i64;
    while d <= 9 {
        let bit = 1i64 << d;
        if (used & bit) == 0 {
            board[pos as usize] = d;
            rows[r as usize] |= bit;
            cols[c as usize] |= bit;
            boxes[b as usize] |= bit;
            if go(board, rows, cols, boxes, pos + 1) {
                return true;
            }
            board[pos as usize] = 0;
            rows[r as usize] ^= bit;
            cols[c as usize] ^= bit;
            boxes[b as usize] ^= bit;
        }
        d += 1;
    }
    false
}

fn solve(board: &mut [i64]) -> bool {
    let mut rows = [0i64; 9];
    let mut cols = [0i64; 9];
    let mut boxes = [0i64; 9];
    let mut i = 0i64;
    while i < 81 {
        let d = board[i as usize];
        if d != 0 {
            let r = i / 9;
            let c = i % 9;
            let bit = 1i64 << d;
            rows[r as usize] |= bit;
            cols[c as usize] |= bit;
            boxes[box_index(r, c) as usize] |= bit;
        }
        i += 1;
    }
    go(board, &mut rows, &mut cols, &mut boxes, 0)
}

fn main() {
    let total: i64 = 500;
    let modulus: i64 = 1000000007;

    let template: [i64; 81] = [
        8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 9, 0, 2, 0, 0,
        0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 4, 5, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0,
        0, 0, 1, 0, 0, 0, 0, 6, 8, 0, 0, 8, 5, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0,
    ];

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let mut work: [i64; 81] = [0; 81];
        let mut j = 0i64;
        while j < 81 {
            work[j as usize] = template[j as usize];
            j += 1;
        }
        work[(k % 81) as usize] = 0;

        solve(&mut work);

        let mut sig: i64 = 0;
        let mut i = 0i64;
        while i < 81 {
            sig += work[i as usize] * (i + 1);
            i += 1;
        }
        acc = (acc * 31 + sig) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
