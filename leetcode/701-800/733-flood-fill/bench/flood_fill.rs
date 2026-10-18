// LeetCode #733: Flood Fill -- depth first, with a stack of places.
// Benchmark mirror of the Kara star arm: push the start; pop a place,
// and if it still has the old color, paint it and push its four
// neighbours.

fn flood_fill(mut img: Vec<Vec<i64>>, sr: i64, sc: i64, color: i64) -> Vec<Vec<i64>> {
    let old = img[sr as usize][sc as usize];
    if old == color {
        return img;
    }
    let m = img.len() as i64;
    let n = img[0].len() as i64;
    let mut stack: Vec<(i64, i64)> = Vec::new();
    stack.push((sr, sc));
    while let Some((r, c)) = stack.pop() {
        if r < 0 || r >= m || c < 0 || c >= n || img[r as usize][c as usize] != old {
            continue;
        }
        img[r as usize][c as usize] = color;
        stack.push((r + 1, c));
        stack.push((r - 1, c));
        stack.push((r, c + 1));
        stack.push((r, c - 1));
    }
    img
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 733;
    let size: i64 = 1000;
    let mut img: Vec<Vec<i64>> = Vec::new();
    for _ in 0..size {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..size {
            row.push(if next_random(&mut seed) % 3 == 0 { 1 } else { 0 });
        }
        img.push(row);
    }
    let mut sum = 0;
    for _ in 0..40 {
        let r = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % size;
        let c = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % size;
        let old = img[r as usize][c as usize];
        img = flood_fill(img, r, c, 2);
        for x in 0..size as usize {
            if img[r as usize][x] == 2 {
                sum += 1;
            }
        }
        img = flood_fill(img, r, c, old);
    }
    let mut zeros = 0;
    for row in img.iter() {
        for &v in row.iter() {
            if v == 0 {
                zeros += 1;
            }
        }
    }
    println!("40 rounds on a 1000 x 1000 image: {} painted in their rows, {} 0s after", sum, zeros);
}
