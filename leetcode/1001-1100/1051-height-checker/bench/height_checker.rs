// LeetCode #1051: Height Checker -- Rust mirror of
// bench/height_checker.kara.

fn height_checker(heights: &[i64]) -> i64 {
    let mut expected = heights.to_vec();
    expected.sort_unstable();
    let mut moved = 0;
    for i in 0..heights.len() {
        if heights[i] != expected[i] {
            moved += 1;
        }
    }
    moved
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (lines, count, rounds) = (2000, 100, 50);
    let mut seed = 1051;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..lines {
        let mut heights = Vec::new();
        for _ in 0..count {
            heights.push(next_random(&mut seed) % 100 + 1);
        }
        all.push(heights);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for heights in &all {
            let answer = height_checker(heights);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{lines} lines of {count} students, {rounds} rounds: total {total}, checksum {check}");
}
