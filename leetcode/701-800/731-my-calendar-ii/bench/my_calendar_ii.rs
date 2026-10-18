// LeetCode #731: My Calendar II -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings and
// the stretches two of them cover, and refuse a booking that meets one
// of those stretches.

struct MyCalendarTwo {
    booked: Vec<(i64, i64)>,
    doubled: Vec<(i64, i64)>,
}

impl MyCalendarTwo {
    fn new() -> MyCalendarTwo {
        MyCalendarTwo { booked: Vec::new(), doubled: Vec::new() }
    }

    fn book(&mut self, start: i64, end: i64) -> bool {
        for d in self.doubled.iter() {
            if start < d.1 && d.0 < end {
                return false;
            }
        }
        for b in self.booked.iter() {
            if start < b.1 && b.0 < end {
                let lo = if start > b.0 { start } else { b.0 };
                let hi = if end < b.1 { end } else { b.1 };
                self.doubled.push((lo, hi));
            }
        }
        self.booked.push((start, end));
        true
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 731;
    let mut lists: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..20 {
        let mut bookings: Vec<(i64, i64)> = Vec::new();
        for _ in 0..1000 {
            let s = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 996999000;
            let len = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 3000000;
            bookings.push((s, s + len));
        }
        lists.push(bookings);
    }
    let mut accepted = 0;
    for round in 0..80i64 {
        for d in 0..20 {
            let mut cal = MyCalendarTwo::new();
            for b in lists[d].iter() {
                if cal.book(b.0 + round, b.1 + round) {
                    accepted += 1;
                }
            }
        }
    }
    println!("80 rounds of 20 lists of 1000 bookings: {} accepted", accepted);
}
