// LeetCode 759 — Employee Free Time: benchmark, the ★ arm in Rust.

#[derive(Clone, Copy)]
struct Interval {
    start: i64,
    end: i64,
}

fn employee_free_time(schedule: &Vec<Vec<Interval>>) -> Vec<Interval> {
    let mut all: Vec<Interval> = Vec::new();
    for employee in schedule {
        for interval in employee {
            all.push(*interval);
        }
    }
    all.sort_by(|x, y| x.start.cmp(&y.start));
    let mut free: Vec<Interval> = Vec::new();
    let mut end = all[0].end;
    for interval in &all {
        if interval.start > end {
            free.push(Interval { start: end, end: interval.start });
        }
        if interval.end > end {
            end = interval.end;
        }
    }
    free
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let rounds = 3000;
    let mut seed = 759;
    let mut gaps: i64 = 0;
    let mut length: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut schedule: Vec<Vec<Interval>> = Vec::new();
        for _ in 0..50 {
            let mut employee: Vec<Interval> = Vec::new();
            let mut t = 0;
            for _ in 0..50 {
                let start = t + wide_random(&mut seed) % 1000000;
                let end = start + 1 + wide_random(&mut seed) % 900000;
                employee.push(Interval { start, end });
                t = end + 1;
            }
            schedule.push(employee);
        }
        let free = employee_free_time(&schedule);
        gaps += free.len() as i64;
        for interval in &free {
            length += interval.end - interval.start;
            check = (check * 31 + interval.start) % 1000000007;
        }
    }
    println!("{rounds} schedules of 50 x 50 intervals: {gaps} free intervals, {length} free in all, checksum {check}");
}
