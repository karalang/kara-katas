// LeetCode #2056: Number of Valid Move Combinations On Chessboard -- Rust
// mirror of the ★ arm's benchmark (moves.kara): the same 200 boards of 4
// pieces, the same moves and backtracking, each new move walked against the
// moves already chosen.

#[derive(Clone, Copy)]
struct Move {
    dr: i64,
    dc: i64,
    steps: i64,
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn moves_of(kind: &str, r: i64, c: i64) -> Vec<Move> {
    let rook = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    let bishop = [(1, 1), (1, -1), (-1, 1), (-1, -1)];
    let mut dirs: Vec<(i64, i64)> = Vec::new();
    if kind != "bishop" {
        dirs.extend(rook.iter());
    }
    if kind != "rook" {
        dirs.extend(bishop.iter());
    }
    let mut moves = vec![Move { dr: 0, dc: 0, steps: 0 }];
    for &(dr, dc) in &dirs {
        let mut steps = 1;
        while (1..=8).contains(&(r + dr * steps)) && (1..=8).contains(&(c + dc * steps)) {
            moves.push(Move { dr, dc, steps });
            steps += 1;
        }
    }
    moves
}

fn collide(a: (i64, i64), ma: Move, b: (i64, i64), mb: Move) -> bool {
    for t in 1..=ma.steps.max(mb.steps) {
        let (ta, tb) = (t.min(ma.steps), t.min(mb.steps));
        if a.0 + ma.dr * ta == b.0 + mb.dr * tb && a.1 + ma.dc * ta == b.1 + mb.dc * tb {
            return true;
        }
    }
    false
}

fn count_from(i: usize, at: &[(i64, i64)], options: &[Vec<Move>], chosen: &mut Vec<Move>) -> i64 {
    if i == at.len() {
        return 1;
    }
    let mut total = 0;
    for &m in &options[i] {
        if (0..i).all(|j| !collide(at[j], chosen[j], at[i], m)) {
            chosen.push(m);
            total += count_from(i + 1, at, options, chosen);
            chosen.pop();
        }
    }
    total
}

fn count_combinations(pieces: &[String], positions: &[(i64, i64)]) -> i64 {
    let options: Vec<Vec<Move>> = (0..pieces.len()).map(|i| moves_of(&pieces[i], positions[i].0, positions[i].1)).collect();
    let mut chosen = Vec::new();
    count_from(0, positions, &options, &mut chosen)
}

fn main() {
    let kinds = ["rook", "queen", "bishop"];
    let mut seed = 2056;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..200 {
        let mut pieces: Vec<String> = Vec::new();
        let mut positions: Vec<(i64, i64)> = Vec::new();
        while positions.len() < 4 {
            let r = next_random(&mut seed) % 8 + 1;
            let c = next_random(&mut seed) % 8 + 1;
            let kind = kinds[(next_random(&mut seed) % 3) as usize].to_string();
            if !positions.contains(&(r, c)) {
                pieces.push(kind);
                positions.push((r, c));
            }
        }
        let count = count_combinations(&pieces, &positions);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    println!("200 boards: sum {total}, checksum {check}");
}
