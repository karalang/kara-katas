// LeetCode #1476: Subrectangle Queries -- bench, Rust mirror of
// subrectangle_queries.kara (LeetCode's Rust signatures: i32 corners,
// cast to usize to index)

struct SubrectangleQueries {
    rect: Vec<Vec<i32>>,
}

impl SubrectangleQueries {
    fn new(rectangle: Vec<Vec<i32>>) -> Self {
        SubrectangleQueries { rect: rectangle }
    }

    fn update_subrectangle(&mut self, row1: i32, col1: i32, row2: i32, col2: i32, new_value: i32) {
        for r in row1..=row2 {
            for c in col1..=col2 {
                self.rect[r as usize][c as usize] = new_value;
            }
        }
    }

    fn get_value(&self, row: i32, col: i32) -> i32 {
        self.rect[row as usize][col as usize]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1476;
    let mut rect: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100 {
        rect.push(
            (0..100)
                .map(|_| {
                    let hi = next_random(&mut seed);
                    (1 + (hi * 32768 + next_random(&mut seed)) % 1000000000) as i32
                })
                .collect(),
        );
    }
    let mut q = SubrectangleQueries::new(rect);
    let mut check: i64 = 0;
    for pass in 0..5000i64 {
        for _ in 0..250 {
            let r1 = next_random(&mut seed) % 100;
            let r2 = r1 + next_random(&mut seed) % (100 - r1);
            let c1 = next_random(&mut seed) % 100;
            let c2 = c1 + next_random(&mut seed) % (100 - c1);
            q.update_subrectangle(r1 as i32, c1 as i32, r2 as i32, c2 as i32, (1 + check % 1000000000) as i32);
            let r = next_random(&mut seed) % 100;
            let c = next_random(&mut seed) % 100;
            check = (check * 31 + q.get_value(r as i32, c as i32) as i64 + pass) % 1000000007;
        }
    }
    println!("5000 passes of 250 updates on 100 by 100: checksum {}", check);
}
