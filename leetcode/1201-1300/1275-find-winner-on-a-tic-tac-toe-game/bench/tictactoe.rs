// LeetCode #1275 bench, in Rust: the ★ arm (line sums) asked about every
// position of every game of tic-tac-toe, 549,945 of them, each game carried
// on while the answer is "Pending"; 40 rounds, every answer folded into a
// checksum.

fn tictactoe(moves: &Vec<Vec<i64>>) -> String {
    let mut rows = [0i64; 3];
    let mut cols = [0i64; 3];
    let mut diagonal = 0i64;
    let mut anti = 0i64;
    let mut turn = 1i64;
    for m in moves.iter() {
        let (r, c) = (m[0] as usize, m[1] as usize);
        rows[r] += turn;
        cols[c] += turn;
        if r == c {
            diagonal += turn;
        }
        if r + c == 2 {
            anti += turn;
        }
        if rows[r].abs() == 3 || cols[c].abs() == 3 || diagonal.abs() == 3 || anti.abs() == 3 {
            return if turn == 1 { "A".to_string() } else { "B".to_string() };
        }
        turn = -turn;
    }
    if moves.len() == 9 { "Draw".to_string() } else { "Pending".to_string() }
}

fn walk(moves: &mut Vec<Vec<i64>>, check: &mut i64) {
    for square in 0..9i64 {
        let (r, c) = (square / 3, square % 3);
        if moves.iter().any(|m| m[0] == r && m[1] == c) {
            continue;
        }
        moves.push(vec![r, c]);
        let answer = tictactoe(moves);
        let k = if answer == "A" { 0 } else if answer == "B" { 1 } else if answer == "Draw" { 2 } else { 3 };
        *check = (*check * 7 + k) % 1000000007;
        if k == 3 {
            walk(moves, check);
        }
        moves.pop();
    }
}

fn main() {
    let mut check = 0i64;
    for round in 0..40 {
        let mut moves: Vec<Vec<i64>> = Vec::new();
        walk(&mut moves, &mut check);
        check = (check * 131 + round) % 1000000007;
    }
    println!("40 rounds of every game: checksum {}", check);
}
