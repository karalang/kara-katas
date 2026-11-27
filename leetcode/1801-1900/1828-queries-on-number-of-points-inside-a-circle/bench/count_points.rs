// LeetCode #1828: Queries on Number of Points Inside a Circle -- the bench in
// Rust: the ★ arm over 200 calls on runs of 250 to 499 points and 250 to 499
// queries cut from one list of 1000 points and one of 1000 queries of radius 1
// to 500, built once, each run's start and lengths drawn from the checksum so
// far. Each call copies its runs, as the arm takes its lists by value.

fn count_points(points: Vec<Vec<i64>>, queries: Vec<Vec<i64>>) -> Vec<i64> {
    let mut answer: Vec<i64> = Vec::new();
    for q in queries.iter() {
        let (x, y, r) = (q[0], q[1], q[2]);
        let mut inside = 0;
        for p in points.iter() {
            let (dx, dy) = (p[0] - x, p[1] - y);
            if dx * dx + dy * dy <= r * r {
                inside += 1;
            }
        }
        answer.push(inside);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1828;
    let mut points: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let x = next_random(&mut seed) % 501;
        points.push(vec![x, next_random(&mut seed) % 501]);
    }
    let mut queries: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let x = next_random(&mut seed) % 501;
        let y = next_random(&mut seed) % 501;
        queries.push(vec![x, y, 1 + next_random(&mut seed) % 500]);
    }
    let mut check: i64 = 0;
    for call in 0..200 {
        let from = ((check + call) % 500) as usize;
        let n = (250 + (check * 7 + call) % 250) as usize;
        let m = (250 + (check * 13 + call) % 250) as usize;
        let answer = count_points(points[from..from + n].to_vec(), queries[from..from + m].to_vec());
        for &c in answer.iter() {
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("200 calls: checksum {}", check);
}
