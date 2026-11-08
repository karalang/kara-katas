// LeetCode #2013: Detect Squares -- the ★ arm's benchmark, a mirror of
// squares.kara.

struct DetectSquares {
    rows: Vec<Vec<i64>>,
    points: Vec<(i64, i64)>,
}

impl DetectSquares {
    fn new() -> Self {
        DetectSquares { rows: vec![Vec::new(); 1001], points: Vec::new() }
    }

    fn at(&self, x: i64, y: i64) -> i64 {
        let row = &self.rows[x as usize];
        if row.is_empty() { 0 } else { row[y as usize] }
    }

    fn add(&mut self, point: (i64, i64)) {
        let (x, y) = (point.0 as usize, point.1 as usize);
        if self.rows[x].is_empty() {
            self.rows[x] = vec![0; 1001];
        }
        if self.rows[x][y] == 0 {
            self.points.push(point);
        }
        self.rows[x][y] += 1;
    }

    fn count(&self, point: (i64, i64)) -> i64 {
        let (x, y) = point;
        let mut ways = 0;
        for &(px, py) in &self.points {
            if px != x && (px - x).abs() == (py - y).abs() {
                ways += self.at(px, py) * self.at(x, py) * self.at(px, y);
            }
        }
        ways
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2013i64;
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for r in 0..20i64 {
        let mut squares = DetectSquares::new();
        for _ in 0..20000 {
            let base = (r % 10) * 90;
            let point = (base + next_random(&mut seed) % 60, base + next_random(&mut seed) % 60);
            if next_random(&mut seed) % 3 == 0 {
                let ways = squares.count(point);
                calls += 1;
                sum += ways;
                check = (check * 31 + ways) % 1000000007;
            } else {
                squares.add(point);
            }
        }
    }
    println!("{calls} counts: sum {sum}, checksum {check}");
}
