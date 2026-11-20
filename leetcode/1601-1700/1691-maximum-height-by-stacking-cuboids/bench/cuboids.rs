// LeetCode #1691: Maximum Height by Stacking Cuboids -- the bench's Rust
// mirror: the ★ arm on 3000 random sets of 100 cuboids, all drawn first,
// each answered 5 times.

fn max_height(cuboids: &[Vec<i32>]) -> i32 {
    let mut boxes: Vec<Vec<i32>> = cuboids
        .iter()
        .map(|c| {
            let mut sides = c.clone();
            sides.sort();
            sides
        })
        .collect();
    boxes.sort();
    let n = boxes.len();
    let mut best = vec![0i32; n];
    let mut tallest = 0;
    for i in 0..n {
        best[i] = boxes[i][2];
        for j in 0..i {
            if boxes[j][0] <= boxes[i][0] && boxes[j][1] <= boxes[i][1] && boxes[j][2] <= boxes[i][2] {
                best[i] = best[i].max(best[j] + boxes[i][2]);
            }
        }
        tallest = tallest.max(best[i]);
    }
    tallest
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 3000;
    let size = 100;
    let rounds = 5;
    let mut seed = 1691;
    let mut sets: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        let mut cuboids = Vec::new();
        for _ in 0..size {
            cuboids.push((0..3).map(|_| (next_random(&mut seed) % 100 + 1) as i32).collect());
        }
        sets.push(cuboids);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for cuboids in sets.iter() {
            let answer = max_height(cuboids) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} sets of {size} cuboids, {rounds} rounds: answers sum to {total}, checksum {check}");
}
