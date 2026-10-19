// LeetCode 794 — Valid Tic-Tac-Toe State: the bench, in Rust. Mirrors
// valid_tic_tac_toe.kara: count the marks and check the lines.

fn wins(cells: &[u8], mark: u8) -> bool {
    let lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
    for line in lines {
        if cells[line[0]] == mark && cells[line[1]] == mark && cells[line[2]] == mark {
            return true;
        }
    }
    false
}

fn valid_tic_tac_toe(board: &[String]) -> bool {
    let mut cells: Vec<u8> = Vec::new();
    for row in board {
        for b in row.bytes() {
            cells.push(b);
        }
    }
    let x = cells.iter().filter(|&&c| c == b'X').count();
    let o = cells.iter().filter(|&&c| c == b'O').count();
    if x != o && x != o + 1 {
        return false;
    }
    if wins(&cells, b'X') && x != o + 1 {
        return false;
    }
    if wins(&cells, b'O') && x != o {
        return false;
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_board(seed: &mut i64) -> Vec<String> {
    let mut cells = vec![' '; 9];
    if next_random(seed) % 2 == 0 {
        let marks = [' ', 'X', 'O'];
        for i in 0..9 {
            cells[i] = marks[(next_random(seed) % 3) as usize];
        }
    } else {
        let moves = next_random(seed) % 10;
        let mut mover = 'X';
        for _ in 0..moves {
            let empty: Vec<usize> = (0..9).filter(|&i| cells[i] == ' ').collect();
            let at = empty[(next_random(seed) % empty.len() as i64) as usize];
            cells[at] = mover;
            mover = if mover == 'X' { 'O' } else { 'X' };
        }
    }
    (0..3).map(|r| cells[r * 3..r * 3 + 3].iter().collect()).collect()
}

fn main() {
    let mut seed = 794;
    let boards: Vec<Vec<String>> = (0..4096).map(|_| random_board(&mut seed)).collect();
    let rounds = 6000000;
    let mut valid = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        if valid_tic_tac_toe(&boards[r % 4096]) {
            valid += 1;
            check = (check * 131 + (r % 4096) as i64) % 1000000007;
        }
    }
    println!("{rounds} boards: {valid} valid, checksum {check}");
}
