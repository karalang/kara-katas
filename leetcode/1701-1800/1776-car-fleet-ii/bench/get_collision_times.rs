// LeetCode #1776: Car Fleet II -- the bench in Rust, mirroring
// get_collision_times.kara: a stack of the cars ahead from the right.

fn catch_time(cars: &[Vec<i32>], i: usize, j: usize) -> f64 {
    (cars[j][0] - cars[i][0]) as f64 / (cars[i][1] - cars[j][1]) as f64
}

fn get_collision_times(cars: &[Vec<i32>]) -> Vec<f64> {
    let n = cars.len();
    let mut answer = vec![-1.0f64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in (0..n).rev() {
        while let Some(&j) = stack.last() {
            if cars[i][1] <= cars[j][1] || (answer[j] > 0.0 && catch_time(cars, i, j) >= answer[j]) {
                stack.pop();
            } else {
                break;
            }
        }
        if let Some(&j) = stack.last() {
            answer[i] = catch_time(cars, i, j);
        }
        stack.push(i);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1776;
    let mut lists: Vec<Vec<Vec<i32>>> = Vec::new();
    for l in 0..20 {
        let fastest = if l % 2 == 0 { 1000000 } else { 100 };
        let mut cars: Vec<Vec<i32>> = Vec::new();
        let mut position: i64 = 0;
        for _ in 0..100000 {
            position += 1 + next_random(&mut seed) % 10;
            let speed = 1 + next_random(&mut seed) % fastest;
            cars.push(vec![position as i32, speed as i32]);
        }
        lists.push(cars);
    }
    let mut check: i64 = 0;
    for call in 0..200i64 {
        let answer = get_collision_times(&lists[((check + call) % 20) as usize]);
        let t = answer[(check % 100000) as usize];
        check = (check * 31 + (t * 100000.0 + 0.5).floor() as i64 + 100001) % 1000000007;
    }
    println!("200 calls over 20 lists: checksum {}", check);
}
