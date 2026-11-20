// LeetCode #1725: Number Of Rectangles That Can Form The Largest Square
// -- the bench (rectangles.kara): one pass, the largest shorter side so
// far and how many rectangles give it.

fn count_good_rectangles(rectangles: &[Vec<i32>]) -> i32 {
    let mut best = 0;
    let mut count = 0;
    for r in rectangles.iter() {
        let side = r[0].min(r[1]);
        if side > best {
            best = side;
            count = 1;
        } else if side == best {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds: i64 = 50;
    let n = 1000;
    let mut seed: i64 = 1725;
    let mut problems: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        let mut rectangles: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let l = next_random(&mut seed) % 20 + 1;
            let w = next_random(&mut seed) % 20 + 1;
            rectangles.push(vec![l as i32, w as i32]);
        }
        problems.push(rectangles);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for rectangles in problems.iter() {
            let answer = count_good_rectangles(rectangles) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} problems of {} rectangles, {} rounds: answers sum to {}, checksum {}",
        count, n, rounds, sum, check
    );
}
