// LeetCode #1301 bench: the ★ arm (a table from the bottom-right corner
// back, each square holding the most points reaching it and how many paths
// collect that many) over 20 boards of 100 by 100 with obstacles 0 to 38 in
// 100, built once; then 150 passes, each setting one square of every board to
// an obstacle or a digit from the checksum so far, answering it, and folding
// the score and the count into the checksum.

fn paths_with_max_score(board: &[String]) -> [i64; 2] {
    let grid: Vec<Vec<char>> = board.iter().map(|row| row.chars().collect()).collect();
    let n = grid.len();
    let modulus = 1000000007;
    let mut best = vec![vec![-1i64; n]; n];
    let mut ways = vec![vec![0i64; n]; n];
    best[n - 1][n - 1] = 0;
    ways[n - 1][n - 1] = 1;
    for i in (0..n).rev() {
        for j in (0..n).rev() {
            if grid[i][j] == 'X' || (i == n - 1 && j == n - 1) {
                continue;
            }
            let mut top = -1;
            let mut count = 0;
            for (a, b) in [(i + 1, j), (i, j + 1), (i + 1, j + 1)] {
                if a < n && b < n && best[a][b] >= 0 {
                    if best[a][b] > top {
                        top = best[a][b];
                        count = ways[a][b];
                    } else if best[a][b] == top {
                        count = (count + ways[a][b]) % modulus;
                    }
                }
            }
            if top >= 0 {
                let points = match grid[i][j].to_digit(10) {
                    Some(d) => d as i64,
                    None => 0,
                };
                best[i][j] = top + points;
                ways[i][j] = count;
            }
        }
    }
    if best[0][0] < 0 {
        [0, 0]
    } else {
        [best[0][0], ways[0][0]]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1301;
    let mut boards: Vec<Vec<String>> = Vec::new();
    for t in 0..20 {
        let wall = 2 * t;
        let mut board: Vec<String> = Vec::new();
        for i in 0..100 {
            let mut row = String::new();
            for j in 0..100 {
                if i == 0 && j == 0 {
                    row.push('E');
                } else if i == 99 && j == 99 {
                    row.push('S');
                } else if next_random(&mut seed) % 100 < wall {
                    row.push('X');
                } else {
                    row.push(char::from_digit((next_random(&mut seed) % 9 + 1) as u32, 10).unwrap());
                }
            }
            board.push(row);
        }
        boards.push(board);
    }
    let mut check: i64 = 0;
    for p in 0..150 {
        for board in boards.iter_mut() {
            let at = 1 + check % 9998;
            let (i, j) = ((at / 100) as usize, (at % 100) as usize);
            let mut cells: Vec<char> = board[i].chars().collect();
            cells[j] = if check % 7 == 0 { 'X' } else { char::from_digit((check % 9 + 1) as u32, 10).unwrap() };
            board[i] = cells.iter().collect();
            let got = paths_with_max_score(board);
            check = (check * 31 + got[0] + p) % 1000000007;
            check = (check * 31 + got[1]) % 1000000007;
        }
    }
    println!("150 passes over 20 boards of 100 by 100: checksum {}", check);
}
