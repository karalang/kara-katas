// LeetCode #2123: Minimum Operations to Remove Adjacent Ones in Matrix --
// the benchmark, the same algorithm as isolated.kara: the ones a bipartite
// graph by the parity of row plus column, the answer a maximum matching
// grown by Kuhn's augmenting paths.

fn try_match(u: usize, adj: &[Vec<usize>], partner: &mut [i64], seen: &mut [i64], stamp: i64) -> bool {
    for &v in &adj[u] {
        if seen[v] == stamp {
            continue;
        }
        seen[v] = stamp;
        if partner[v] < 0 || try_match(partner[v] as usize, adj, partner, seen, stamp) {
            partner[v] = u as i64;
            return true;
        }
    }
    false
}

fn minimum_operations(grid: &[Vec<i64>]) -> i64 {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); (rows * cols) as usize];
    for r in 0..rows {
        for c in 0..cols {
            if grid[r as usize][c as usize] == 0 || (r + c) % 2 != 0 {
                continue;
            }
            for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
                let (nr, nc) = (r + dr, c + dc);
                if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr as usize][nc as usize] == 1 {
                    adj[(r * cols + c) as usize].push((nr * cols + nc) as usize);
                }
            }
        }
    }
    let cells = (rows * cols) as usize;
    let mut partner = vec![-1i64; cells];
    let mut seen = vec![-1i64; cells];
    let mut matched = 0;
    for u in 0..cells {
        if !adj[u].is_empty() && try_match(u, &adj, &mut partner, &mut seen, u as i64) {
            matched += 1;
        }
    }
    matched
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2123;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..12 {
        let chance = [1, 2, 3][g % 3];
        let mut grid = Vec::new();
        for _ in 0..300 {
            let mut row = Vec::new();
            for _ in 0..300 {
                row.push(if next_random(&mut seed) % 4 < chance { 1 } else { 0 });
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for round in 0..10usize {
        for g in 0..12usize {
            let cell = (round * 7919 + g * 104729) % 90000;
            grids[g][cell / 300][cell % 300] = 1 - grids[g][cell / 300][cell % 300];
            let got = minimum_operations(&grids[g]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("120 solves: {} operations, checksum {}", total, check);
}
