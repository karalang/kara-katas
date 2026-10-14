// LeetCode #630: Course Schedule III -- Rust mirror of the Kāra bench.
//
// The ★ arm's greedy over the same inputs and rounds: the courses
// cloned and sorted by last day, and a `BinaryHeap` of the durations
// taken.

use std::collections::BinaryHeap;

fn schedule_course(courses: &Vec<Vec<i64>>) -> i64 {
    let mut order = courses.clone();
    order.sort_by(|a, b| a[1].cmp(&b[1]));
    let mut taken = BinaryHeap::new();
    let mut time = 0;
    for course in &order {
        time += course[0];
        taken.push(course[0]);
        if time > course[1] {
            time -= taken.pop().unwrap();
        }
    }
    taken.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 20;
    let rounds = 200;
    let mut seed: i64 = 630;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..inputs {
        let longest = 10 + next_random(&mut seed) % 991;
        let mut courses = Vec::new();
        for _ in 0..10000 {
            let duration = 1 + next_random(&mut seed) % longest;
            let last = 1 + next_random(&mut seed) % 10000;
            courses.push(vec![duration, last]);
        }
        all.push(courses);
    }
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let c = schedule_course(&all[(r * 7) % inputs]);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    println!("{} inputs, {} rounds: total {}, checksum {}", inputs, rounds, sum, checksum);
}
