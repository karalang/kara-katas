// LeetCode #2728: Count Houses in a Circular Street -- the bench in Rust:
// the ★ arm over 300 streets of up to 1000 houses with k = 1000, all
// drawn first, then each walked 500 times through the judge's street,
// whose moves are counted.

struct Street {
    doors: Vec<bool>,
    at: usize,
    moves: i64,
}

impl Street {
    fn open_door(&mut self) {
        self.doors[self.at] = true;
    }
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
    for _ in 0..k {
        street.close_door();
        street.move_right();
    }
    street.open_door();
    let mut houses = 1;
    street.move_right();
    while !street.is_door_open() {
        houses += 1;
        street.move_right();
    }
    houses
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 300;
    let rounds = 500;
    let mut rng = Rng(2728);
    let mut streets = Vec::new();
    for _ in 0..count {
        let n = rng.next_random() % 1000 + 1;
        let doors: Vec<bool> = (0..n).map(|_| rng.next_random() % 2 == 0).collect();
        let at = (rng.next_random() % n) as usize;
        streets.push(Street { doors, at, moves: 0 });
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for street in streets.iter_mut() {
            let a = house_count(street, 1000);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    let moves: i64 = streets.iter().map(|s| s.moves).sum();
    println!("{count} streets, {rounds} rounds: houses sum to {total} in {moves} moves, checksum {check}");
}
