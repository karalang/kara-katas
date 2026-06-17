// LeetCode #36 bench — Rust (mirror of valid_sudoku.kara).
//
// Single-pass bitmask validation of a 9×9 board with three stack `[i64; 9]` mask
// arrays, perturb-validate-restore TOTAL times with the verdict folded into a
// checksum. `rustc -O` wraps on overflow; the bench also builds a
// `-C overflow-checks=on` variant to match Kāra's checked-by-default semantics
// (all values stay well inside i64, so neither variant traps — the safety tax
// isolates codegen).

fn box_index(r: i64, c: i64) -> i64 {
    (r / 3) * 3 + c / 3
}

fn is_valid(board: &[i64]) -> bool {
    let mut rows = [0i64; 9];
    let mut cols = [0i64; 9];
    let mut boxes = [0i64; 9];
    let mut r = 0i64;
    while r < 9 {
        let mut c = 0i64;
        while c < 9 {
            let d = board[(r * 9 + c) as usize];
            if d != 0 {
                let bit = 1i64 << d;
                let b = box_index(r, c);
                if (rows[r as usize] & bit) != 0
                    || (cols[c as usize] & bit) != 0
                    || (boxes[b as usize] & bit) != 0
                {
                    return false;
                }
                rows[r as usize] |= bit;
                cols[c as usize] |= bit;
                boxes[b as usize] |= bit;
            }
            c += 1;
        }
        r += 1;
    }
    true
}

fn main() {
    let total: i64 = 5000000;
    let modulus: i64 = 1000000007;

    let mut board: [i64; 81] = [
        5, 3, 4, 6, 7, 8, 9, 1, 2, 6, 7, 2, 1, 9, 5, 3, 4, 8, 1, 9, 8, 3, 4, 2, 5, 6, 7, 8, 5, 9,
        7, 6, 1, 4, 2, 3, 4, 2, 6, 8, 5, 3, 7, 9, 1, 7, 1, 3, 9, 2, 4, 8, 5, 6, 9, 6, 1, 5, 3, 7,
        2, 8, 4, 2, 8, 7, 4, 1, 9, 6, 3, 5, 3, 4, 5, 2, 8, 6, 1, 7, 9,
    ];

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let pos = (k % 81) as usize;
        let digit = (k % 9) + 1;
        let save = board[pos];
        board[pos] = digit;
        let v: i64 = if is_valid(&board) { 1 } else { 0 };
        acc = (acc * 31 + v) % modulus;
        board[pos] = save;
        k += 1;
    }

    println!("{}", acc);
}
