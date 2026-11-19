// LeetCode #1659: Maximize Grid Happiness -- the bench's Rust mirror: the
// ★ arm on 2000 random problems on grids of 4 to 5 rows by 4 to 5 columns
// with up to 6 introverts and 6 extroverts, all drawn first.

const INTROVERT: i64 = 1;
const EXTROVERT: i64 = 2;

fn pair(a: i64, b: i64) -> i64 {
    if a == 0 || b == 0 {
        return 0;
    }
    let mut score = 0;
    for p in [a, b] {
        score += if p == INTROVERT { -30 } else { 20 };
    }
    score
}

struct Grid {
    m: i64,
    n: i64,
    top: i64,
    memo: Vec<i64>,
}

impl Grid {
    fn best(&mut self, cell: i64, introverts: i64, extroverts: i64, last: i64) -> i64 {
        if cell == self.m * self.n || (introverts == 0 && extroverts == 0) {
            return 0;
        }
        let key = (((cell * 7 + introverts) * 7 + extroverts) * self.top + last) as usize;
        if self.memo[key] >= 0 {
            return self.memo[key];
        }
        let up = last / (self.top / 3);
        let left = if cell % self.n == 0 { 0 } else { last % 3 };
        let shifted = last % (self.top / 3) * 3;
        let mut best = self.best(cell + 1, introverts, extroverts, shifted);
        if introverts > 0 {
            let gain = 120 + pair(INTROVERT, up) + pair(INTROVERT, left);
            best = best.max(gain + self.best(cell + 1, introverts - 1, extroverts, shifted + INTROVERT));
        }
        if extroverts > 0 {
            let gain = 40 + pair(EXTROVERT, up) + pair(EXTROVERT, left);
            best = best.max(gain + self.best(cell + 1, introverts, extroverts - 1, shifted + EXTROVERT));
        }
        self.memo[key] = best;
        best
    }
}

fn get_max_grid_happiness(m: i32, n: i32, introverts_count: i32, extroverts_count: i32) -> i32 {
    let m = m as i64;
    let n = n as i64;
    let mut top = 1;
    for _ in 0..n {
        top *= 3;
    }
    let mut grid = Grid { m, n, top, memo: vec![-1; (m * n * 49 * top) as usize] };
    grid.best(0, introverts_count as i64, extroverts_count as i64, 0) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1659;
    let mut problems: Vec<(i32, i32, i32, i32)> = Vec::new();
    for _ in 0..2000 {
        let m = (next_random(&mut seed) % 2 + 4) as i32;
        let n = (next_random(&mut seed) % 2 + 4) as i32;
        let introverts = (next_random(&mut seed) % 7) as i32;
        let extroverts = (next_random(&mut seed) % 7) as i32;
        problems.push((m, n, introverts, extroverts));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &(m, n, introverts, extroverts) in &problems {
        let answer = get_max_grid_happiness(m, n, introverts, extroverts) as i64;
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("2000 grids of 4 to 5 by 4 to 5: happiness sums to {}, checksum {}", total, check);
}
