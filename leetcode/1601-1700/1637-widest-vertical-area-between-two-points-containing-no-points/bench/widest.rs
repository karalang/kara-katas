// LeetCode #1637: Widest Vertical Area Between Two Points Containing No
// Points -- the bench's Rust mirror: the ★ arm on 40 random sets of 100000
// points with x and y from 0 to 10^9, all drawn first.

fn max_width_of_vertical_area(points: &Vec<Vec<i32>>) -> i32 {
    let mut xs: Vec<i32> = points.iter().map(|p| p[0]).collect();
    xs.sort();
    xs.windows(2).map(|w| w[1] - w[0]).max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1637;
    let mut sets: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..40 {
        let mut points = Vec::new();
        for _ in 0..100000 {
            let x = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001;
            let y = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001;
            points.push(vec![x as i32, y as i32]);
        }
        sets.push(points);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for points in &sets {
        let width = max_width_of_vertical_area(points) as i64;
        total += width;
        check = (check * 31 + width + 1) % 1000000007;
    }
    println!("40 sets of 100000 points: widths sum to {}, checksum {}", total, check);
}
