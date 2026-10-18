// LeetCode #732: My Calendar III -- starts and ends, merged.
// Benchmark mirror of the Kara star arm: keep the starts and the ends
// in two sorted vectors, each put in its place by binary search, and
// sweep both together for the most bookings at once.

struct MyCalendarThree {
    starts: Vec<i64>,
    ends: Vec<i64>,
}

fn place(v: &mut Vec<i64>, x: i64) {
    let mut lo = 0;
    let mut hi = v.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if v[mid] <= x {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    v.insert(lo, x);
}

impl MyCalendarThree {
    fn new() -> MyCalendarThree {
        MyCalendarThree { starts: Vec::new(), ends: Vec::new() }
    }

    fn book(&mut self, start: i64, end: i64) -> i64 {
        place(&mut self.starts, start);
        place(&mut self.ends, end);
        let n = self.starts.len();
        let mut i = 0;
        let mut j = 0;
        let mut now = 0;
        let mut most = 0;
        while i < n {
            if self.ends[j] <= self.starts[i] {
                now -= 1;
                j += 1;
            } else {
                now += 1;
                i += 1;
                if now > most {
                    most = now;
                }
            }
        }
        most
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 732;
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
    let mut sum: i64 = 0;
    for round in 0..40i64 {
        for d in 0..20 {
            let mut cal = MyCalendarThree::new();
            for b in lists[d].iter() {
                sum += cal.book(b.0 + round, b.1 + round);
            }
        }
    }
    println!("40 rounds of 20 lists of 1000 bookings: answers sum {}", sum);
}
