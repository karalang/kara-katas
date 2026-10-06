// Bench mirror of snake_game.kara (the grid + ring-buffer arm), same algorithm.
const ROUNDS: i64 = 30;
const WIDTH: i64 = 1000;
const HEIGHT: i64 = 400;

struct SnakeGame {
    width: i64,
    height: i64,
    food: Vec<(i64, i64)>,
    next_food: i64,
    ring: Vec<i64>,
    start: i64,
    len: i64,
    covered: Vec<bool>,
}

impl SnakeGame {
    fn new(width: i64, height: i64, food: Vec<(i64, i64)>) -> SnakeGame {
        let cap = (width * height) as usize;
        let mut covered = vec![false; cap];
        covered[0] = true;
        SnakeGame { width, height, food, next_food: 0, ring: vec![0; cap], start: 0, len: 1, covered }
    }

    fn step(&mut self, dir: u8) -> i64 {
        let cap = self.ring.len() as i64;
        let head = self.ring[((self.start + self.len - 1) % cap) as usize];
        let (r, c) = (head / self.width, head % self.width);
        let (nr, nc) = match dir {
            b'U' => (r - 1, c),
            b'D' => (r + 1, c),
            b'L' => (r, c - 1),
            _ => (r, c + 1),
        };
        if nr < 0 || nr >= self.height || nc < 0 || nc >= self.width {
            return -1;
        }
        let cell = nr * self.width + nc;
        if self.next_food < self.food.len() as i64 && self.food[self.next_food as usize] == (nr, nc) {
            self.next_food += 1;
        } else {
            let tail = self.ring[self.start as usize];
            self.covered[tail as usize] = false;
            self.start = (self.start + 1) % cap;
            self.len -= 1;
        }
        if self.covered[cell as usize] {
            return -1;
        }
        self.ring[((self.start + self.len) % cap) as usize] = cell;
        self.len += 1;
        self.covered[cell as usize] = true;
        self.next_food
    }
}

fn main() {
    let mut sink: i64 = 0;
    for round in 0..ROUNDS {
        let (w, h) = (WIDTH, HEIGHT + 2 * round);
        let n = w * h;
        let mut moves: Vec<u8> = Vec::new();
        for _ in 0..w - 1 {
            moves.push(b'R');
        }
        for row in 1..h {
            moves.push(b'D');
            let d = if row % 2 == 1 { b'L' } else { b'R' };
            for _ in 0..w - 2 {
                moves.push(d);
            }
        }
        moves.push(b'L');
        for _ in 0..h - 1 {
            moves.push(b'U');
        }
        let mut food: Vec<(i64, i64)> = Vec::new();
        let (mut r, mut c, mut t) = (0i64, 0i64, 0usize);
        while (food.len() as i64) < n / 4 {
            match moves[t] {
                b'U' => r -= 1,
                b'D' => r += 1,
                b'L' => c -= 1,
                _ => c += 1,
            }
            if t % 3 == 2 {
                food.push((r, c));
            }
            t += 1;
        }
        let mut g = SnakeGame::new(w, h, food);
        for t in 0..3 * n {
            let s = g.step(moves[(t % n) as usize]);
            sink = (sink * 31 + s + t) % 1000000007;
        }
        sink = (sink + g.len) % 1000000007;
    }
    println!("{}", sink);
}
