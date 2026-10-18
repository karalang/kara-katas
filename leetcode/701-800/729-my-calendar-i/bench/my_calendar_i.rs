// LeetCode #729: My Calendar I -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings in
// a list and accept a new one only if it overlaps none of them.

struct MyCalendar {
    booked: Vec<(i64, i64)>,
}

impl MyCalendar {
    fn new() -> MyCalendar {
        MyCalendar { booked: Vec::new() }
    }

    fn book(&mut self, start: i64, end: i64) -> bool {
        for b in self.booked.iter() {
            if start < b.1 && b.0 < end {
                return false;
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
    let mut seed: i64 = 729;
    let mut lists: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..20 {
        let mut bookings: Vec<(i64, i64)> = Vec::new();
        for _ in 0..1000 {
            let s = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 998999000;
            let len = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000;
            bookings.push((s, s + len));
        }
        lists.push(bookings);
    }
    let mut accepted = 0;
    for round in 0..80i64 {
        for d in 0..20 {
            let mut cal = MyCalendar::new();
            for b in lists[d].iter() {
                if cal.book(b.0 + round, b.1 + round) {
                    accepted += 1;
                }
            }
        }
    }
    println!("80 rounds of 20 lists of 1000 bookings: {} accepted", accepted);
}
