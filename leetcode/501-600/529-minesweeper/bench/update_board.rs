// Benchmark for #529: Rust mirror of the ★ arm (reveal recursively); see
// update_board.kara. The same seeded generator, so the same boards and
// clicks; a fresh clone of the board per click.

fn mines_around(board: &Vec<Vec<char>>, r: i64, c: i64) -> i64 {
    let mut count = 0;
    for dr in -1..=1 {
        for dc in -1..=1 {
            let (y, x) = (r + dr, c + dc);
            if (dr != 0 || dc != 0) && y >= 0 && y < board.len() as i64 && x >= 0 && x < board[0].len() as i64 {
                let v = board[y as usize][x as usize];
                if v == 'M' || v == 'X' {
                    count += 1;
                }
            }
        }
    }
    count
}

fn reveal(board: &mut Vec<Vec<char>>, r: i64, c: i64) {
    if board[r as usize][c as usize] != 'E' {
        return;
    }
    let count = mines_around(board, r, c);
    if count > 0 {
        board[r as usize][c as usize] = (48 + count) as u8 as char;
        return;
    }
    board[r as usize][c as usize] = 'B';
    for dr in -1..=1 {
        for dc in -1..=1 {
            let (y, x) = (r + dr, c + dc);
            if y >= 0 && y < board.len() as i64 && x >= 0 && x < board[0].len() as i64 {
                reveal(board, y, x);
            }
        }
    }
}

fn update_board(mut board: Vec<Vec<char>>, click: Vec<i64>) -> Vec<Vec<char>> {
    let (r, c) = (click[0], click[1]);
    if board[r as usize][c as usize] == 'M' {
        board[r as usize][c as usize] = 'X';
    } else {
        reveal(&mut board, r, c);
    }
    board
}

fn main() {
    let mut seed: i64 = 529;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut boards: Vec<Vec<Vec<char>>> = Vec::new();
    for _ in 0..50 {
        let percent = next_random() % 21;
        let mut board: Vec<Vec<char>> = Vec::new();
        for _ in 0..50 {
            let mut row: Vec<char> = Vec::new();
            for _ in 0..50 {
                row.push(if next_random() % 100 < percent { 'M' } else { 'E' });
            }
            board.push(row);
        }
        boards.push(board);
    }
    let (mut opened, mut exploded, mut checksum) = (0i64, 0i64, 0i64);
    for _ in 0..400 {
        for b in 0..boards.len() {
            let r = next_random() % 50;
            let c = next_random() % 50;
            let after = update_board(boards[b].clone(), vec![r, c]);
            let mut shown = 0;
            for row in after.iter() {
                for ch in row.iter() {
                    if *ch == 'X' {
                        exploded += 1;
                    } else if *ch != 'E' && *ch != 'M' {
                        shown += 1;
                    }
                }
            }
            opened += shown;
            checksum = (checksum * 31 + shown) % 1000000007;
        }
    }
    println!("50 boards of 50 by 50, 400 rounds of clicks: {} opened, {} exploded, checksum {}", opened, exploded, checksum);
}
