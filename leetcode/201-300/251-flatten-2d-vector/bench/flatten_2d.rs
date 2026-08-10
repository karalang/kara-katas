// Benchmark workload for LeetCode #251 — Flatten 2D Vector (Rust mirror).
// Mirrors flatten_2d.kara algorithm-for-algorithm.

struct Vector2D<'a> {
    data: &'a Vec<Vec<i64>>,
    row: usize,
    col: usize,
}

impl<'a> Vector2D<'a> {
    fn skip_empty(&mut self) {
        while self.row < self.data.len() && self.col >= self.data[self.row].len() {
            self.row += 1;
            self.col = 0;
        }
    }
    fn has_next(&mut self) -> bool {
        self.skip_empty();
        self.row < self.data.len()
    }
    fn next(&mut self) -> i64 {
        self.skip_empty();
        if self.row >= self.data.len() {
            return -1;
        }
        let x = self.data[self.row][self.col];
        self.col += 1;
        x
    }
}

fn main() {
    let rows: i64 = 20000;
    let passes: i64 = 1500;

    let mut data: Vec<Vec<i64>> = Vec::new();
    let mut state: i64 = 251251;
    for _ in 0..rows {
        state = (state * 1103515245 + 12345) & 2147483647;
        let mut row: Vec<i64> = Vec::new();
        if (state / 65536) % 100 >= 45 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let cols = (state / 65536) % 6 + 1;
            for _ in 0..cols {
                state = (state * 1103515245 + 12345) & 2147483647;
                row.push((state / 65536) % 1000);
            }
        }
        data.push(row);
    }

    let mut sink: i64 = 0;
    for _ in 0..passes {
        let mut v = Vector2D { data: &data, row: 0, col: 0 };
        while v.has_next() {
            let x = v.next();
            sink = (sink * 31 + x + 1) % 1000000007;
        }
    }
    println!("{}", sink);
}
