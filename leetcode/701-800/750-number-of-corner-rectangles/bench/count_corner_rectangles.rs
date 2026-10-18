// LeetCode 750 — Number Of Corner Rectangles, bench: the ★ arm (pairs
// of rows) on a 200 x 200 grid that keeps changing.
// Mirrors count_corner_rectangles.kara.

fn count_corner_rectangles(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let n = grid[0].len();
    let mut total = 0i64;
    for a in 0..m {
        for b in a + 1..m {
            let mut k = 0i64;
            for c in 0..n {
                if grid[a][c] == 1 && grid[b][c] == 1 {
                    k += 1;
                }
            }
            total += k * (k - 1) / 2;
        }
    }
    total
}

struct Rng(i64);
impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 100;
    let mut rng = Rng(750);
    let mut grid: Vec<Vec<i64>> = (0..200).map(|_| (0..200).map(|_| rng.next() % 2).collect()).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for _ in 0..50 {
            let r = (rng.next() % 200) as usize;
            let c = (rng.next() % 200) as usize;
            grid[r][c] = rng.next() % 2;
        }
        let k = count_corner_rectangles(&grid);
        total += k;
        check = (check * 31 + k) % 1000000007;
    }
    println!("{} grids of 200 x 200: {} rectangles in all, checksum {}", rounds, total, check);
}
