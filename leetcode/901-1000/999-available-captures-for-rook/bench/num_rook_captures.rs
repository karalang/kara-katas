// Benchmark: LeetCode #999 Available Captures for Rook -- the ★ arm, a
// walk from the rook each way, on random 8 by 8 boards. Mirrors
// num_rook_captures.kara, .c, .py and go-seq/. The board is LeetCode's
// Rust shape, `Vec<Vec<char>>`.

fn num_rook_captures(board: &[Vec<char>]) -> i64 {
    let mut rr: i64 = 0;
    let mut rc: i64 = 0;
    for r in 0..8 {
        for c in 0..8 {
            if board[r][c] == 'R' {
                rr = r as i64;
                rc = c as i64;
            }
        }
    }
    let mut captures = 0;
    for (dr, dc) in [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)].iter() {
        let mut r = rr + dr;
        let mut c = rc + dc;
        while r >= 0 && r < 8 && c >= 0 && c < 8 {
            if board[r as usize][c as usize] == 'p' {
                captures += 1;
                break;
            }
            if board[r as usize][c as usize] == 'B' {
                break;
            }
            r += dr;
            c += dc;
        }
    }
    captures
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 500000;
    let mut seed = 999;
    // 20 boards, the rook on a random square and each other square a pawn
    // 4 times in 16 and a bishop 2 times in 16
    let mut boards: Vec<Vec<Vec<char>>> = Vec::new();
    for _ in 0..20 {
        let rook = next_random(&mut seed) % 64;
        let mut board: Vec<Vec<char>> = Vec::new();
        for r in 0..8 {
            let mut row: Vec<char> = Vec::new();
            for c in 0..8 {
                let x = next_random(&mut seed) % 16;
                row.push(if r * 8 + c == rook {
                    'R'
                } else if x < 4 {
                    'p'
                } else if x < 6 {
                    'B'
                } else {
                    '.'
                });
            }
            board.push(row);
        }
        boards.push(board);
    }
    let mut captures: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let k = ((r + i) % 20) as usize;
            let got = num_rook_captures(&boards[k]);
            captures += got;
            check = (check * 31 + got + 1) % 1000000007;
            // a pawn put on or taken off one square, so no board stays put
            let s = ((r * 13 + i * 5) % 64) as usize;
            let cell = &mut boards[k][s / 8][s % 8];
            if *cell == '.' {
                *cell = 'p';
            } else if *cell == 'p' {
                *cell = '.';
            }
        }
    }
    println!("{} rounds over 20 boards: {} captures, checksum {}", rounds, captures, check);
}
