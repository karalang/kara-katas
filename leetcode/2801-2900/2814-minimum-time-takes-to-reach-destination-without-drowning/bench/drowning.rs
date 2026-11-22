// LeetCode #2814: Minimum Time Takes to Reach Destination Without
// Drowning -- the bench in Rust: the ★ arm over 200 lands of 100 by 100,
// a cell in five stone and one in 5000 flooded, all drawn first, then
// each answered 5 times. The land is a `Vec<Vec<String>>` as in Kāra.
use std::collections::VecDeque;

const DIRS: [(i64, i64); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn minimum_seconds(land: &[Vec<String>]) -> i64 {
    let (n, m) = (land.len() as i64, land[0].len() as i64);
    let at = |r: i64, c: i64| land[r as usize][c as usize].as_str();
    let mut flood = vec![vec![i64::MAX; m as usize]; n as usize];
    let mut queue = VecDeque::new();
    for r in 0..n {
        for c in 0..m {
            if at(r, c) == "*" {
                flood[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in DIRS {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0
                && nr < n
                && nc >= 0
                && nc < m
                && flood[nr as usize][nc as usize] == i64::MAX
                && (at(nr, nc) == "." || at(nr, nc) == "S")
            {
                flood[nr as usize][nc as usize] = flood[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
            }
        }
    }
    let mut time = vec![vec![-1i64; m as usize]; n as usize];
    for r in 0..n {
        for c in 0..m {
            if at(r, c) == "S" {
                time[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        if at(r, c) == "D" {
            return time[r as usize][c as usize];
        }
        for (dr, dc) in DIRS {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0
                && nr < n
                && nc >= 0
                && nc < m
                && time[nr as usize][nc as usize] == -1
                && at(nr, nc) != "X"
                && flood[nr as usize][nc as usize] > time[r as usize][c as usize] + 1
            {
                time[nr as usize][nc as usize] = time[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
            }
        }
    }
    -1
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 200;
    let rounds = 5;
    let n = 100i64;
    let mut rng = Rng(2814);
    let mut lands: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..count {
        let mut land: Vec<Vec<String>> = Vec::new();
        for _ in 0..n {
            let mut row: Vec<String> = Vec::new();
            for _ in 0..n {
                let roll = rng.next_random() % 10000;
                row.push(if roll < 2000 { "X" } else if roll < 2002 { "*" } else { "." }.to_string());
            }
            land.push(row);
        }
        let start = rng.next_random() % (n * n);
        let mut end = rng.next_random() % (n * n - 1);
        if end >= start {
            end += 1;
        }
        land[(start / n) as usize][(start % n) as usize] = "S".to_string();
        land[(end / n) as usize][(end % n) as usize] = "D".to_string();
        lands.push(land);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for land in &lands {
            let a = minimum_seconds(land);
            total += a;
            check = (check * 31 + a + 2 + r) % 1000000007;
        }
    }
    println!("{count} lands of {n} by {n}, {rounds} rounds: seconds sum to {total}, checksum {check}");
}
