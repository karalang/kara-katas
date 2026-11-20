// LeetCode #1274 bench, in Rust: the ★ arm (divide and conquer by
// quarters through the sea's interface) on 500 random seas of 10 ships in
// the whole 1001-by-1001 square and 10 more in a corner, drawn once, 30
// rounds; every count, and the number of questions asked, folded into a
// checksum.

use std::cell::Cell;

trait Sea {
    fn has_ships(&self, top_right: Vec<i64>, bottom_left: Vec<i64>) -> bool;
}

struct Ocean {
    ships: Vec<(i64, i64)>,
    calls: Cell<i64>,
}

impl Sea for Ocean {
    fn has_ships(&self, top_right: Vec<i64>, bottom_left: Vec<i64>) -> bool {
        self.calls.set(self.calls.get() + 1);
        self.ships
            .iter()
            .any(|&(x, y)| bottom_left[0] <= x && x <= top_right[0] && bottom_left[1] <= y && y <= top_right[1])
    }
}

fn count_ships(sea: &dyn Sea, top_right: Vec<i64>, bottom_left: Vec<i64>) -> i64 {
    if bottom_left[0] > top_right[0] || bottom_left[1] > top_right[1] {
        return 0;
    }
    if !sea.has_ships(top_right.clone(), bottom_left.clone()) {
        return 0;
    }
    if top_right == bottom_left {
        return 1;
    }
    let mx = (top_right[0] + bottom_left[0]) / 2;
    let my = (top_right[1] + bottom_left[1]) / 2;
    count_ships(sea, vec![mx, my], bottom_left.clone())
        + count_ships(sea, vec![top_right[0], my], vec![mx + 1, bottom_left[1]])
        + count_ships(sea, vec![mx, top_right[1]], vec![bottom_left[0], my + 1])
        + count_ships(sea, top_right, vec![mx + 1, my + 1])
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1274;
    let mut seas: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..500 {
        let mut ships: Vec<(i64, i64)> = Vec::new();
        for i in 0..20 {
            let span = if i < 10 { 1001 } else { 30 };
            let x = next_random(&mut seed) % span;
            let p = (x, next_random(&mut seed) % span);
            if !ships.contains(&p) {
                ships.push(p);
            }
        }
        seas.push(ships);
    }
    let mut check: i64 = 0;
    for round in 0..30 {
        for ships in &seas {
            let sea = Ocean { ships: ships.clone(), calls: Cell::new(0) };
            let n = count_ships(&sea, vec![1000, 1000], vec![0, 0]);
            check = (check * 131 + n + round) % 1000000007;
            check = (check * 131 + sea.calls.get()) % 1000000007;
        }
    }
    println!("30 rounds of 500 seas: checksum {}", check);
}
