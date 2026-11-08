// LeetCode #1504: Count Submatrices With All Ones -- the benchmark, the
// same algorithm as submat.kara: column heights per row and a stack of
// increasing heights.

fn count_submatrices(mat: Vec<Vec<i64>>) -> i64 {
    let m = mat.len();
    let n = mat[0].len();
    let mut heights = vec![0i64; n];
    let mut total = 0;
    for i in 0..m {
        for j in 0..n {
            heights[j] = if mat[i][j] == 1 { heights[j] + 1 } else { 0 };
        }
        let mut ending = vec![0i64; n];
        let mut stack: Vec<usize> = Vec::new();
        for j in 0..n {
            while !stack.is_empty() && heights[stack[stack.len() - 1]] >= heights[j] {
                stack.pop();
            }
            ending[j] = if stack.is_empty() {
                heights[j] * (j as i64 + 1)
            } else {
                let k = stack[stack.len() - 1];
                ending[k] + heights[j] * (j - k) as i64
            };
            stack.push(j);
            total += ending[j];
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_square(size: i64, ones: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    (0..size)
        .map(|_| (0..size).map(|_| if next_random(seed) % 100 < ones { 1 } else { 0 }).collect())
        .collect()
}

fn main() {
    let mut seed = 1504;
    let mats: Vec<Vec<Vec<i64>>> = (0..400).map(|i| random_square(150, 50 + i % 50, &mut seed)).collect();
    let (mut total, mut check) = (0, 0);
    for mat in &mats {
        let answer = count_submatrices(mat.clone());
        total += answer;
        check = mix(check, answer);
    }
    println!("400 matrices of 150 x 150: sum {total}, checksum {check}");
}
