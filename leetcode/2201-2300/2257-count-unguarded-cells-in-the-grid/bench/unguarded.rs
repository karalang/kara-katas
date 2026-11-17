// LeetCode #2257: Count Unguarded Cells in the Grid -- the benchmark's
// Rust mirror of unguarded.kara: a grid of marks and a walk from every
// guard in each of the four directions until a wall, a guard or the edge.

fn count_unguarded(m: i64, n: i64, guards: &[[i64; 2]], walls: &[[i64; 2]]) -> i64 {
    // 0 empty, 1 seen, 2 guard, 3 wall
    let mut grid = vec![vec![0u8; n as usize]; m as usize];
    for g in guards {
        grid[g[0] as usize][g[1] as usize] = 2;
    }
    for w in walls {
        grid[w[0] as usize][w[1] as usize] = 3;
    }
    for g in guards {
        for (dr, dc) in [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)] {
            let mut r = g[0] + dr;
            let mut c = g[1] + dc;
            while r >= 0 && r < m && c >= 0 && c < n && grid[r as usize][c as usize] < 2 {
                grid[r as usize][c as usize] = 1;
                r += dr;
                c += dc;
            }
        }
    }
    grid.iter().map(|row| row.iter().filter(|&&cell| cell == 0).count() as i64).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn place(seed: &mut i64, m: i64, n: i64, guards: usize, walls: usize) -> (Vec<[i64; 2]>, Vec<[i64; 2]>) {
    let mut taken = vec![false; (m * n) as usize];
    let mut cells: Vec<[i64; 2]> = Vec::new();
    while cells.len() < guards + walls {
        let k = wide_random(seed) % (m * n);
        if !taken[k as usize] {
            taken[k as usize] = true;
            cells.push([k / n, k % n]);
        }
    }
    let rest = cells.split_off(guards);
    (cells, rest)
}

fn main() {
    let mut seed = 2257i64;
    let mut check = 0i64;
    let shapes = [(1i64, 100000i64), (250, 400), (100000, 1)];
    for t in 0..300 {
        let (m, n) = shapes[t % 3];
        let (guards, walls) = place(&mut seed, m, n, 2000, 10000);
        check = (check * 31 + count_unguarded(m, n, &guards, &walls) + 1) % 1000000007;
    }
    println!("300 grids of 10^5 cells: checksum {}", check);
}
