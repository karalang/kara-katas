// Benchmark workload for LeetCode #348 — Rust mirror of tic_tac_toe.kara.

const SIDE: i64 = 1000;
const GAMES: i64 = 100;

struct TicTacToe {
    n: i64,
    rows: Vec<i64>,
    cols: Vec<i64>,
    diag: i64,
    anti: i64,
}

impl TicTacToe {
    fn new(n: i64) -> TicTacToe {
        TicTacToe { n, rows: vec![0; n as usize], cols: vec![0; n as usize], diag: 0, anti: 0 }
    }

    fn make_move(&mut self, row: i64, col: i64, player: i64) -> i64 {
        let d = if player == 1 { 1 } else { -1 };
        self.rows[row as usize] += d;
        self.cols[col as usize] += d;
        if row == col {
            self.diag += d;
        }
        if row + col == self.n - 1 {
            self.anti += d;
        }
        let goal = d * self.n;
        if self.rows[row as usize] == goal
            || self.cols[col as usize] == goal
            || self.diag == goal
            || self.anti == goal
        {
            return player;
        }
        0
    }
}

fn main() {
    let cells = SIDE * SIDE;
    let mut order: Vec<i64> = (0..cells).collect();
    let mut x: i64 = 348;
    let mut k = cells - 1;
    while k > 0 {
        x = (x * 1103515245 + 12345) % 2147483648;
        let j = x / 16 % (k + 1);
        order.swap(k as usize, j as usize);
        k -= 1;
    }

    let mut sink: i64 = 0;
    for g in 0..GAMES {
        let start = g * cells / GAMES;
        let mut game = TicTacToe::new(SIDE);
        let mut player = 1;
        let mut moves = 0;
        let mut winner = 0;
        while moves < cells && winner == 0 {
            let cell = order[((start + moves) % cells) as usize];
            winner = game.make_move(cell / SIDE, cell % SIDE, player);
            moves += 1;
            player = 3 - player;
        }
        sink = (sink * 31 + moves * (winner + 1)) % 1000000007;
    }
    println!("sink {}", sink);
}
