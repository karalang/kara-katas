// LeetCode #1700: Number of Students Unable to Eat Lunch -- the bench's
// Rust mirror: the ★ arm on 50000 random lunches of 100 students, all
// drawn first, each answered 80 times.

fn count_students(students: &[i32], sandwiches: &[i32]) -> i32 {
    let mut wanting = [0, 0];
    for &s in students.iter() {
        wanting[s as usize] += 1;
    }
    for &s in sandwiches.iter() {
        if wanting[s as usize] == 0 {
            break;
        }
        wanting[s as usize] -= 1;
    }
    wanting[0] + wanting[1]
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50000;
    let rounds = 80;
    let n = 100;
    let mut seed = 1700;
    let mut lunches: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..count {
        let lean = next_random(&mut seed) % 11;
        let mut students: Vec<i32> = Vec::new();
        let mut sandwiches: Vec<i32> = Vec::new();
        for _ in 0..n {
            students.push(if next_random(&mut seed) % 10 < lean { 1 } else { 0 });
        }
        for _ in 0..n {
            sandwiches.push(if next_random(&mut seed) % 10 < lean { 1 } else { 0 });
        }
        lunches.push((students, sandwiches));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (students, sandwiches) in lunches.iter() {
            let answer = count_students(students, sandwiches) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} lunches of {n} students, {rounds} rounds: answers sum to {total}, checksum {check}");
}
