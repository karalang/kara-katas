// LeetCode 764 — Largest Plus Sign: benchmark, the ★ arm in Rust.
// 300 random grids of 500 x 500 with 5,000 mines each.

fn order_of_largest_plus_sign(n: usize, mines: &[Vec<usize>]) -> i64 {
    let mut grid = vec![vec![n as i64; n]; n];
    for mine in mines {
        grid[mine[0]][mine[1]] = 0;
    }
    for i in 0..n {
        let (mut left, mut right, mut up, mut down) = (0i64, 0i64, 0i64, 0i64);
        for j in 0..n {
            left = if grid[i][j] == 0 { 0 } else { left + 1 };
            grid[i][j] = grid[i][j].min(left);
            let k = n - 1 - j;
            right = if grid[i][k] == 0 { 0 } else { right + 1 };
            grid[i][k] = grid[i][k].min(right);
            up = if grid[j][i] == 0 { 0 } else { up + 1 };
            grid[j][i] = grid[j][i].min(up);
            down = if grid[k][i] == 0 { 0 } else { down + 1 };
            grid[k][i] = grid[k][i].min(down);
        }
    }
    grid.iter().flat_map(|row| row.iter()).copied().max().unwrap_or(0)
}

fn main() {
    let mut seed: i64 = 764;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds = 300;
    let n = 500usize;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut taken = vec![false; n * n];
        let mut mines: Vec<Vec<usize>> = Vec::new();
        while mines.len() < 5000 {
            let r = (next_random() % n as i64) as usize;
            let c = (next_random() % n as i64) as usize;
            if !taken[r * n + c] {
                taken[r * n + c] = true;
                mines.push(vec![r, c]);
            }
        }
        let order = order_of_largest_plus_sign(n, &mines);
        total += order;
        check = (check * 31 + order) % 1000000007;
    }
    println!("{} grids of 500 x 500 with 5000 mines: orders adding up to {}, checksum {}", rounds, total, check);
}
