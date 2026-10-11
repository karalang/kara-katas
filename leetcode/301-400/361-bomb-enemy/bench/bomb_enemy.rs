// Benchmark for #361 -- mirror of bomb_enemy.kara.

fn max_killed_enemies(grid: &[String]) -> i64 {
    let rows = grid.len();
    if rows == 0 {
        return 0;
    }
    let cells: Vec<Vec<u8>> = grid.iter().map(|r| r.bytes().collect()).collect();
    let cols = cells[0].len();
    let mut best = 0;
    let mut row_hits = 0;
    let mut col_hits = vec![0i64; cols];
    for i in 0..rows {
        for j in 0..cols {
            if j == 0 || cells[i][j - 1] == b'W' {
                row_hits = 0;
                let mut k = j;
                while k < cols && cells[i][k] != b'W' {
                    if cells[i][k] == b'E' {
                        row_hits += 1;
                    }
                    k += 1;
                }
            }
            if i == 0 || cells[i - 1][j] == b'W' {
                col_hits[j] = 0;
                let mut k = i;
                while k < rows && cells[k][j] != b'W' {
                    if cells[k][j] == b'E' {
                        col_hits[j] += 1;
                    }
                    k += 1;
                }
            }
            if cells[i][j] == b'0' {
                best = best.max(row_hits + col_hits[j]);
            }
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 361;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for _ in 0..60 {
        let mut grid: Vec<String> = Vec::new();
        for _ in 0..400 {
            let mut row = String::with_capacity(400);
            for _ in 0..400 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                let r = (seed / 65536) % 6;
                row.push(if r == 0 { 'W' } else if r < 3 { 'E' } else { '0' });
            }
            grid.push(row);
        }
        let best = max_killed_enemies(&grid);
        total += best;
        checksum = (checksum * 31 + best) % 1000000007;
    }
    println!("60 grids: {} enemies in total, checksum {}", total, checksum);
}
