// LeetCode #419: Battleships in a Board -- Rust mirror of
// battleships.kara (count the first cells).

fn count_battleships(board: &[Vec<char>]) -> i64 {
    let mut count = 0;
    for r in 0..board.len() {
        for c in 0..board[r].len() {
            if board[r][c] == 'X' && (r == 0 || board[r - 1][c] != 'X') && (c == 0 || board[r][c - 1] != 'X') {
                count += 1;
            }
        }
    }
    count
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn clear(board: &[Vec<char>], r: i64, c: i64) -> bool {
    let n = board.len() as i64;
    let around = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)];
    for (rr, cc) in around {
        if rr >= 0 && rr < n && cc >= 0 && cc < n && board[rr as usize][cc as usize] == 'X' {
            return false;
        }
    }
    true
}

fn main() {
    let n: i64 = 200;
    let rounds = 20000;
    let mut seed: i64 = 419;
    let mut board: Vec<Vec<char>> = vec![vec!['.'; n as usize]; n as usize];
    for _ in 0..4000 {
        let length = 1 + step(&mut seed) % 4;
        let across = step(&mut seed) % 2 == 0;
        let r = step(&mut seed) % n;
        let c = step(&mut seed) % n;
        let (dr, dc) = if across { (0, 1) } else { (1, 0) };
        let mut fits = r + dr * (length - 1) < n && c + dc * (length - 1) < n;
        for k in 0..length {
            if fits && !clear(&board, r + dr * k, c + dc * k) {
                fits = false;
            }
        }
        if fits {
            for k in 0..length {
                board[(r + dr * k) as usize][(c + dc * k) as usize] = 'X';
            }
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let r = (step(&mut seed) % n) as usize;
        let c = (step(&mut seed) % n) as usize;
        if board[r][c] == 'X' {
            board[r][c] = '.';
            if !clear(&board, r as i64, c as i64) {
                board[r][c] = 'X';
            }
        } else if clear(&board, r as i64, c as i64) {
            board[r][c] = 'X';
        }
        let answer = count_battleships(&board);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{rounds} rounds on a {n}x{n} board: total {total}, checksum {checksum}");
}
