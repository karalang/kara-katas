// LeetCode #739: Daily Temperatures -- a stack of colder days.
// Benchmark mirror of the Kara star arm: walk the days keeping a stack
// of the days still waiting; a day warmer than the top answers it, and
// every day under it that it is warmer than, and then waits itself.

fn daily_temperatures(temperatures: &Vec<i64>) -> Vec<i64> {
    let n = temperatures.len();
    let mut answer: Vec<i64> = Vec::new();
    for _ in 0..n {
        answer.push(0);
    }
    let mut waiting: Vec<usize> = Vec::new();
    for i in 0..n {
        while !waiting.is_empty() && temperatures[waiting[waiting.len() - 1]] < temperatures[i] {
            let j = waiting.pop().unwrap();
            answer[j] = (i - j) as i64;
        }
        waiting.push(i);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 739;
    let n: i64 = 100000;
    let mut t: Vec<i64> = Vec::new();
    for _ in 0..n {
        t.push(30 + next_random(&mut seed) % 71);
    }
    let mut total: i64 = 0;
    for _ in 0..300 {
        for _ in 0..100 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let j = ((a * 32768 + b) % n) as usize;
            t[j] = 30 + next_random(&mut seed) % 71;
        }
        let answer = daily_temperatures(&t);
        for a in answer.iter() {
            total += *a;
        }
    }
    println!("300 rounds of 100000 days: {} days waited in all", total);
}
