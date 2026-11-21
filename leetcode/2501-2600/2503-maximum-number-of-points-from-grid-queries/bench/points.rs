// LeetCode #2503: Maximum Number of Points From Grid Queries -- Rust
// mirror of the benchmark (points.kara): the same grids, queries, passes
// and checksum; the border in a std `BinaryHeap` of `Reverse((value,
// cell))`.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn max_points(grid: &[Vec<i64>], queries: &[i64]) -> Vec<i64> {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by_key(|&i| queries[i]);
    let mut answer = vec![0i64; queries.len()];
    let mut seen = vec![vec![false; n as usize]; m as usize];
    let mut border = BinaryHeap::new();
    border.push(Reverse((grid[0][0], 0i64)));
    seen[0][0] = true;
    let mut reached = 0;
    for &i in &order {
        let q = queries[i];
        while let Some(&Reverse((value, cell))) = border.peek() {
            if value >= q {
                break;
            }
            border.pop();
            reached += 1;
            let (r, c) = (cell / n, cell % n);
            for (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
                let (rr, cc) = (r + dr, c + dc);
                if rr >= 0 && rr < m && cc >= 0 && cc < n && !seen[rr as usize][cc as usize] {
                    seen[rr as usize][cc as usize] = true;
                    border.push(Reverse((grid[rr as usize][cc as usize], rr * n + cc)));
                }
            }
        }
        answer[i] = reached;
    }
    answer
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn below(&mut self, top: i64) -> i64 {
        let hi = self.next();
        (hi * 32768 + self.next()) % top
    }
}

fn main() {
    let passes = 14;
    let mut rng = Rng(2503);
    let mut grids: Vec<Vec<Vec<i64>>> = (0..4)
        .map(|_| (0..316).map(|_| (0..316).map(|_| rng.below(1000000) + 1).collect()).collect())
        .collect();
    let queries: Vec<i64> = (0..10000).map(|_| rng.below(1000000) + 1).collect();
    let mut check: i64 = 0;
    for p in 0..passes {
        for g in 0..4 {
            let r = (check % 316) as usize;
            let c = (check / 316 % 316) as usize;
            let was = grids[g][r][c];
            grids[g][r][c] = (check + p) % 1000000 + 1;
            for a in max_points(&grids[g], &queries) {
                check = (check * 31 + a + p) % 1000000007;
            }
            grids[g][r][c] = was;
        }
    }
    println!("{} passes over 4 grids of 316 by 316, 10^4 queries: checksum {}", passes, check);
}
