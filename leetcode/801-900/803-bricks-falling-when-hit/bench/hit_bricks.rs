// LeetCode 803 -- Bricks Falling When Hit: the bench, mirroring
// hit_bricks.kara with the same union-find run backwards.

const DR: [i64; 4] = [-1, 1, 0, 0];
const DC: [i64; 4] = [0, 0, -1, 1];

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn union(parent: &mut Vec<i64>, size: &mut Vec<i64>, a: i64, b: i64) {
    let ra = find(parent, a);
    let rb = find(parent, b);
    if ra == rb {
        return;
    }
    if size[ra as usize] < size[rb as usize] {
        parent[ra as usize] = rb;
        size[rb as usize] += size[ra as usize];
    } else {
        parent[rb as usize] = ra;
        size[ra as usize] += size[rb as usize];
    }
}

// Join the brick at (r, c) to the roof if it is in the top row, and to
// each brick next to it.
fn join(r: i64, c: i64, rows: i64, cols: i64, left: &[Vec<i64>], parent: &mut Vec<i64>, size: &mut Vec<i64>) {
    let here = r * cols + c;
    if r == 0 {
        union(parent, size, here, rows * cols);
    }
    for d in 0..4 {
        let nr = r + DR[d];
        let nc = c + DC[d];
        if nr >= 0 && nr < rows && nc >= 0 && nc < cols && left[nr as usize][nc as usize] == 1 {
            union(parent, size, here, nr * cols + nc);
        }
    }
}

fn hit_bricks(grid: &[Vec<i64>], hits: &[(i64, i64)]) -> Vec<i64> {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut left = grid.to_vec();
    for &(r, c) in hits.iter() {
        left[r as usize][c as usize] = 0;
    }
    let roof = rows * cols;
    let mut parent: Vec<i64> = Vec::new();
    let mut size: Vec<i64> = Vec::new();
    for i in 0..roof + 1 {
        parent.push(i);
        size.push(1);
    }
    for r in 0..rows {
        for c in 0..cols {
            if left[r as usize][c as usize] == 1 {
                join(r, c, rows, cols, &left, &mut parent, &mut size);
            }
        }
    }
    let mut fallen: Vec<i64> = vec![0; hits.len()];
    for k in (0..hits.len()).rev() {
        let (r, c) = hits[k];
        if grid[r as usize][c as usize] == 1 {
            let before = size[find(&mut parent, roof) as usize];
            left[r as usize][c as usize] = 1;
            join(r, c, rows, cols, &left, &mut parent, &mut size);
            let after = size[find(&mut parent, roof) as usize];
            fallen[k] = (after - before - 1).max(0);
        }
    }
    fallen
}

// The wall with every brick that is not held up from the top row taken
// away, so that every brick starts held up.
fn settled(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut out = vec![vec![0i64; cols as usize]; rows as usize];
    let mut stack: Vec<(i64, i64)> = Vec::new();
    for c in 0..cols {
        if grid[0][c as usize] == 1 {
            out[0][c as usize] = 1;
            stack.push((0, c));
        }
    }
    while let Some((r, c)) = stack.pop() {
        for d in 0..4 {
            let nr = r + DR[d];
            let nc = c + DC[d];
            if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr as usize][nc as usize] == 1 && out[nr as usize][nc as usize] == 0 {
                out[nr as usize][nc as usize] = 1;
                stack.push((nr, nc));
            }
        }
    }
    out
}

fn main() {
    let size: i64 = 200;
    let mut seed: i64 = 803;
    let mut walls: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut all_hits: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..8 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..size {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..size {
                row.push(if next_random(&mut seed) % 4 < 3 { 1 } else { 0 });
            }
            grid.push(row);
        }
        walls.push(settled(&grid));
        let mut cells: Vec<i64> = (0..size * size).collect();
        for j in 1..size * size {
            let t = next_random(&mut seed) % (j + 1);
            cells.swap(j as usize, t as usize);
        }
        let hits: Vec<(i64, i64)> = (0..20000).map(|j| (cells[j] / size, cells[j] % size)).collect();
        all_hits.push(hits);
    }
    let rounds: i64 = 500;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let fallen = hit_bricks(&walls[(r % 8) as usize], &all_hits[(r % 8) as usize]);
        let sum: i64 = fallen.iter().sum();
        total += sum;
        check = (check * 131 + sum + fallen[(r % 20000) as usize]) % 1000000007;
    }
    println!("{} rounds of 20000 hits: {} bricks fell, checksum {}", rounds, total, check);
}
