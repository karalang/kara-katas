fn largest_rect(heights: &[i64]) -> i64 {
    let n = heights.len() as i64;
    let mut stack: Vec<i64> = Vec::new();
    let mut best = 0i64;
    let mut i = 0i64;
    while i <= n {
        let h = if i == n { 0 } else { heights[i as usize] };
        while !stack.is_empty() && heights[*stack.last().unwrap() as usize] >= h {
            let top = *stack.last().unwrap();
            let height = heights[top as usize];
            stack.pop();
            let width = if stack.is_empty() {
                i
            } else {
                i - *stack.last().unwrap() - 1
            };
            let area = height * width;
            if area > best {
                best = area;
            }
        }
        stack.push(i);
        i += 1;
    }
    best
}

fn maximal_rectangle(matrix: &[Vec<i64>], rows: i64, cols: i64) -> i64 {
    let mut heights: Vec<i64> = vec![0i64; cols as usize];
    let mut best = 0i64;
    for r in 0..rows {
        for c in 0..cols {
            if matrix[r as usize][c as usize] == 1 {
                heights[c as usize] += 1;
            } else {
                heights[c as usize] = 0;
            }
        }
        let a = largest_rect(&heights);
        if a > best {
            best = a;
        }
    }
    best
}

fn main() {
    let rows: i64 = 70;
    let cols: i64 = 70;
    let passes: i64 = 11000;

    let mut matrix: Vec<Vec<i64>> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..rows {
        let mut rowv: Vec<i64> = Vec::new();
        for _ in 0..cols {
            state = (state * 1103515245 + 12345) & 2147483647;
            if (state >> 16) % 100 < 62 {
                rowv.push(1);
            } else {
                rowv.push(0);
            }
        }
        matrix.push(rowv);
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        let rr = (p % rows) as usize;
        let cc = ((p * 131 + 7) % cols) as usize;
        matrix[rr][cc] = 1 - matrix[rr][cc];
        sink += maximal_rectangle(&matrix, rows, cols);
    }
    println!("{}", sink);
}
