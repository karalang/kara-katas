// LeetCode #2282: Number of People That Can Be Seen in a Grid -- the
// bench, the ★ arm.

// how many each person in `line` sees farther along it
fn sightings(line: &[i64]) -> Vec<i64> {
    let mut seen: Vec<i64> = vec![0; line.len()];
    let mut stack: Vec<i64> = Vec::new();
    for i in (0..line.len()).rev() {
        let h = line[i];
        while !stack.is_empty() && stack[stack.len() - 1] < h {
            stack.pop();
            seen[i] += 1;
        }
        if !stack.is_empty() {
            seen[i] += 1;
            if stack[stack.len() - 1] == h {
                stack.pop();
            }
        }
        stack.push(h);
    }
    seen
}

fn see_people(heights: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let (m, n) = (heights.len(), heights[0].len());
    let mut answer: Vec<Vec<i64>> = Vec::new();
    for i in 0..m {
        answer.push(sightings(&heights[i]));
    }
    for j in 0..n {
        let column: Vec<i64> = (0..m).map(|i| heights[i][j]).collect();
        let down = sightings(&column);
        for i in 0..m {
            answer[i][j] += down[i];
        }
    }
    answer
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2282;
    let mut check = 0;
    for _ in 0..40 {
        let mut heights: Vec<Vec<i64>> = Vec::new();
        for _ in 0..400 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..400 {
                let top = next_random(&mut seed);
                row.push((top * 32768 + next_random(&mut seed)) % 100000 + 1);
            }
            heights.push(row);
        }
        let answer = see_people(&heights);
        let mut seen = 0;
        for row in &answer {
            for &a in row {
                seen += a;
            }
        }
        check = (check * 31 + seen) % 1000000007;
    }
    println!("40 grids of 400 by 400: checksum {check}");
}
