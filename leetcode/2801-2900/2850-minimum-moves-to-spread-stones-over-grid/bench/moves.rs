// LeetCode #2850: Minimum Moves to Spread Stones Over Grid -- the
// bench: the ★ arm over every grid of nine stones, 24310 of them, all
// made first, then each answered 5 times.

fn spread(k: usize, from: &Vec<(i64, i64)>, to: &Vec<(i64, i64)>, used: &mut Vec<bool>) -> i64 {
    if k == from.len() {
        return 0;
    }
    let (r, c) = from[k];
    let mut best = i64::MAX;
    for j in 0..to.len() {
        if !used[j] {
            used[j] = true;
            let (tr, tc) = to[j];
            best = best.min((r - tr).abs() + (c - tc).abs() + spread(k + 1, from, to, used));
            used[j] = false;
        }
    }
    best
}

fn minimum_moves(grid: &Vec<Vec<i64>>) -> i64 {
    let mut from: Vec<(i64, i64)> = Vec::new();
    let mut to: Vec<(i64, i64)> = Vec::new();
    for r in 0..3 {
        for c in 0..3 {
            if grid[r][c] == 0 {
                to.push((r as i64, c as i64));
            }
            for _ in 1..grid[r][c] {
                from.push((r as i64, c as i64));
            }
        }
    }
    let mut used = vec![false; to.len()];
    spread(0, &from, &to, &mut used)
}

fn every(cell: usize, left: i64, counts: &mut Vec<i64>, out: &mut Vec<Vec<Vec<i64>>>) {
    if cell == 8 {
        counts[8] = left;
        let grid: Vec<Vec<i64>> = (0..3).map(|r| (0..3).map(|c| counts[r * 3 + c]).collect()).collect();
        out.push(grid);
        return;
    }
    for k in 0..left + 1 {
        counts[cell] = k;
        every(cell + 1, left - k, counts, out);
    }
}

fn main() {
    let rounds = 5;
    let mut counts: Vec<i64> = vec![0; 9];
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    every(0, 9, &mut counts, &mut grids);
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for grid in grids.iter() {
            let moves = minimum_moves(grid);
            total += moves;
            check = (check * 31 + moves + r) % 1000000007;
        }
    }
    println!("{} grids, {rounds} rounds: {total} moves, checksum {check}", grids.len());
}
