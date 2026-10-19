// Benchmark for #782: Transform to Chessboard -- mirror of the ★ arm (the
// corner rule and two counts), with the same workload as the Kāra program.

fn moves_to_chessboard(board: &[Vec<i64>]) -> i64 {
    let n = board.len();
    for r in 0..n {
        for c in 0..n {
            if board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c] == 1 {
                return -1;
            }
        }
    }
    let n = n as i64;
    let mut row_ones = 0;
    let mut col_ones = 0;
    let mut row_off = 0;
    let mut col_off = 0;
    for i in 0..n {
        row_ones += board[0][i as usize];
        col_ones += board[i as usize][0];
        if board[i as usize][0] == i % 2 {
            row_off += 1;
        }
        if board[0][i as usize] == i % 2 {
            col_off += 1;
        }
    }
    if row_ones != n / 2 && row_ones != (n + 1) / 2 {
        return -1;
    }
    if col_ones != n / 2 && col_ones != (n + 1) / 2 {
        return -1;
    }
    if n % 2 == 1 {
        if row_off % 2 == 1 {
            row_off = n - row_off;
        }
        if col_off % 2 == 1 {
            col_off = n - col_off;
        }
    } else {
        if n - row_off < row_off {
            row_off = n - row_off;
        }
        if n - col_off < col_off {
            col_off = n - col_off;
        }
    }
    (row_off + col_off) / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let n = 30usize;
    let mut seed: i64 = 782;
    let mut boards: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let mut row_of: Vec<i64> = (0..n as i64).collect();
        let mut col_of: Vec<i64> = (0..n as i64).collect();
        let mut i = n - 1;
        while i > 0 {
            let j = next_random(&mut seed) as usize % (i + 1);
            row_of.swap(i, j);
            let j = next_random(&mut seed) as usize % (i + 1);
            col_of.swap(i, j);
            i -= 1;
        }
        let mut board: Vec<Vec<i64>> = (0..n).map(|r| (0..n).map(|c| (row_of[r] + col_of[c]) % 2).collect()).collect();
        if g % 4 == 1 {
            let r = next_random(&mut seed) as usize % n;
            let c = next_random(&mut seed) as usize % n;
            board[r][c] = 1 - board[r][c];
        } else if g % 4 == 3 {
            for c in 0..n {
                board[0][c] = next_random(&mut seed) % 2;
            }
            for r in 1..n {
                let flip = next_random(&mut seed) % 2;
                for c in 0..n {
                    board[r][c] = board[0][c] ^ flip;
                }
            }
        }
        boards.push(board);
    }
    let mut solvable: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..2000000i64 {
        let g = (round * 7) % count;
        let answer = moves_to_chessboard(&boards[g as usize]);
        if answer >= 0 {
            solvable += 1;
        }
        checksum = (checksum * 31 + answer + 2 + g) % 1000000007;
    }
    println!("2000000 rounds of 30 x 30 boards: {solvable} solvable, checksum {checksum}");
}
