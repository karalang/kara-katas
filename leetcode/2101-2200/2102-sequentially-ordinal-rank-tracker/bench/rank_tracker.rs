// LeetCode #2102: Sequentially Ordinal Rank Tracker -- Rust mirror of the
// ★ arm's benchmark (rank_tracker.kara): the same 20 runs of 4 * 10^4
// calls, two heaps of a Place with its own Ord (greater is better); the
// served heap holds `Reverse(Place)` so its worst is on top.
use std::cmp::{Ordering, Reverse};
use std::collections::{BinaryHeap, HashSet};

#[derive(PartialEq, Eq)]
struct Place {
    score: i64,
    name: String,
}

impl PartialOrd for Place {
    fn partial_cmp(&self, other: &Place) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Place {
    fn cmp(&self, other: &Place) -> Ordering {
        self.score.cmp(&other.score).then(other.name.cmp(&self.name))
    }
}

struct SORTracker {
    served: BinaryHeap<Reverse<Place>>,
    waiting: BinaryHeap<Place>,
}

impl SORTracker {
    fn new() -> SORTracker {
        SORTracker { served: BinaryHeap::new(), waiting: BinaryHeap::new() }
    }

    fn add(&mut self, name: String, score: i64) {
        self.served.push(Reverse(Place { score, name }));
        let Reverse(worst) = self.served.pop().unwrap();
        self.waiting.push(worst);
    }

    fn get(&mut self) -> String {
        let best = self.waiting.pop().unwrap();
        let name = best.name.clone();
        self.served.push(Reverse(best));
        name
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2102;
    let mut gets = 0;
    let mut check: i64 = 0;
    for _ in 0..20 {
        let mut taken: HashSet<String> = HashSet::new();
        let mut tracker = SORTracker::new();
        let mut added = 0;
        let mut asked = 0;
        while asked < 20000 {
            if added < 20000 && (asked == added || next_random(&mut seed) % 2 == 0) {
                let name = loop {
                    let len = next_random(&mut seed) % 10 + 1;
                    let name: String = (0..len).map(|_| (b'a' + (next_random(&mut seed) % 26) as u8) as char).collect();
                    if taken.insert(name.clone()) {
                        break name;
                    }
                };
                let score = wide_random(&mut seed) % 100000 + 1;
                tracker.add(name, score);
                added += 1;
            } else {
                let name = tracker.get();
                asked += 1;
                gets += 1;
                for b in name.bytes() {
                    check = (check * 31 + b as i64) % 1000000007;
                }
                check = (check * 31 + 7) % 1000000007;
            }
        }
    }
    println!("20 runs: {gets} gets, checksum {check}");
}
