// LeetCode #1845: Seat Reservation Manager -- the bench in Rust: the ★ arm,
// every unreserved seat in a `BinaryHeap` of `Reverse`, over 50 runs of 10^5
// calls on 50000 to 99999 seats, each run's size and its place in one list
// of 10^6 draws, built once, taken from the checksum so far. A draw reserves
// a seat two times in three, and otherwise gives back a held seat it picks;
// every seat reserved goes into the checksum.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct SeatManager {
    free: BinaryHeap<Reverse<i64>>,
}

impl SeatManager {
    fn new(n: i64) -> SeatManager {
        SeatManager { free: (1..=n).map(Reverse).collect() }
    }

    fn reserve(&mut self) -> i64 {
        self.free.pop().unwrap().0
    }

    fn unreserve(&mut self, seat_number: i64) {
        self.free.push(Reverse(seat_number));
    }
}

fn main() {
    let mut seed: i64 = 1845;
    let mut draws: Vec<i64> = Vec::new();
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        draws.push(seed / 65536);
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        let n = 50000 + check % 50000;
        let start = (check % 500000) as usize;
        let mut seats = SeatManager::new(n);
        let mut held: Vec<i64> = Vec::new();
        for k in 0..100000 {
            let d = draws[start + k];
            if held.is_empty() || (d % 3 != 0 && (held.len() as i64) < n) {
                let seat = seats.reserve();
                check = (check * 31 + seat) % 1000000007;
                held.push(seat);
            } else {
                let i = (d % held.len() as i64) as usize;
                let seat = held.swap_remove(i);
                seats.unreserve(seat);
            }
        }
    }
    println!("50 runs: checksum {}", check);
}
