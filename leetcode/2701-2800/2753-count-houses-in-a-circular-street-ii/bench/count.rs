// LeetCode #2753: Count Houses in a Circular Street II -- the bench in
// Rust: the ★ arm over 30 streets of up to 10^5 houses with k = 10^5,
// all drawn first, then each walked 20 times, every walk on a fresh copy
// of its street, the walk closing the doors it meets.

struct Street {
    doors: Vec<bool>,
    at: usize,
    moves: i64,
}

impl Street {
    fn close_door(&mut self) {
        self.doors[self.at] = false;
    }
    fn is_door_open(&self) -> bool {
        self.doors[self.at]
    }
    fn move_right(&mut self) {
        self.at = (self.at + 1) % self.doors.len();
        self.moves += 1;
    }
}

fn house_count(street: &mut Street, k: i64) -> i64 {
    while !street.is_door_open() {
        street.move_right();
    }
    let mut last = 0;
    for step in 1..=k {
        street.move_right();
        if street.is_door_open() {
            street.close_door();
            last = step;
        }
    }
    last
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 30;
    let rounds = 20;
    let k = 100000i64;
    let mut rng = Rng(2753);
    let mut cases = Vec::new();
    for _ in 0..count {
        let n = rng.next_random() % k + 1;
        let mut doors: Vec<bool> = (0..n).map(|_| rng.next_random() % 2 == 0).collect();
        let open = (rng.next_random() % n) as usize;
        doors[open] = true;
        let at = (rng.next_random() % n) as usize;
        cases.push((doors, at));
    }
    let mut total = 0i64;
    let mut moves = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (doors, at) in &cases {
            let mut street = Street { doors: doors.clone(), at: *at, moves: 0 };
            let a = house_count(&mut street, k);
            total += a;
            moves += street.moves;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} streets, {rounds} rounds: houses sum to {total} in {moves} moves, checksum {check}");
}
