// LeetCode #2782: Number of Unique Categories -- the bench in Rust: the ★
// arm over 1000 sets of 100 elements from up to 100 categories, all
// drawn first, then each answered 100 times through the judge's handler,
// whose questions are counted.

struct CategoryHandler {
    categories: Vec<i64>,
    asked: i64,
}

impl CategoryHandler {
    fn have_same_category(&mut self, a: i64, b: i64) -> bool {
        self.asked += 1;
        let n = self.categories.len() as i64;
        a >= 0 && b >= 0 && a < n && b < n && self.categories[a as usize] == self.categories[b as usize]
    }
}

fn number_of_categories(n: i64, handler: &mut CategoryHandler) -> i64 {
    let mut representatives: Vec<i64> = Vec::new();
    for i in 0..n {
        if !representatives.iter().any(|&r| handler.have_same_category(r, i)) {
            representatives.push(i);
        }
    }
    representatives.len() as i64
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 1000;
    let rounds = 100;
    let mut rng = Rng(2782);
    let mut handlers = Vec::new();
    for _ in 0..count {
        let k = rng.next_random() % 100 + 1;
        let categories: Vec<i64> = (0..100).map(|_| rng.next_random() % k).collect();
        handlers.push(CategoryHandler { categories, asked: 0 });
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for handler in handlers.iter_mut() {
            let a = number_of_categories(100, handler);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    let asked: i64 = handlers.iter().map(|h| h.asked).sum();
    println!("{count} sets of 100, {rounds} rounds: categories sum to {total} after {asked} questions, checksum {check}");
}
