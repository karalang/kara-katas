fn num_islands(grid: &mut [i64], rows: i64, cols: i64) -> i64 {
    let mut count: i64 = 0;
    let mut r: i64 = 0;
    while r < rows {
        let mut c: i64 = 0;
        while c < cols {
            if grid[(r * cols + c) as usize] == 1 {
                count += 1;
                let mut stack: Vec<i64> = Vec::new();
                stack.push(r * cols + c);
                grid[(r * cols + c) as usize] = 0;
                while !stack.is_empty() {
                    let idx = stack.pop().unwrap();
                    let cr = idx / cols;
                    let cc = idx % cols;
                    if cr > 0 && grid[((cr - 1) * cols + cc) as usize] == 1 {
                        grid[((cr - 1) * cols + cc) as usize] = 0;
                        stack.push((cr - 1) * cols + cc);
                    }
                    if cr + 1 < rows && grid[((cr + 1) * cols + cc) as usize] == 1 {
                        grid[((cr + 1) * cols + cc) as usize] = 0;
                        stack.push((cr + 1) * cols + cc);
                    }
                    if cc > 0 && grid[(cr * cols + (cc - 1)) as usize] == 1 {
                        grid[(cr * cols + (cc - 1)) as usize] = 0;
                        stack.push(cr * cols + (cc - 1));
                    }
                    if cc + 1 < cols && grid[(cr * cols + (cc + 1)) as usize] == 1 {
                        grid[(cr * cols + (cc + 1)) as usize] = 0;
                        stack.push(cr * cols + (cc + 1));
                    }
                }
            }
            c += 1;
        }
        r += 1;
    }
    count
}

fn main() {
    let rows: i64 = 80;
    let cols: i64 = 80;
    let passes: i64 = 13000;
    let total = rows * cols;

    let mut master: Vec<i64> = Vec::with_capacity(total as usize);
    let mut state: i64 = 12345;
    for _ in 0..total {
        state = (state * 1103515245 + 12345) & 2147483647;
        master.push(if (state >> 16) % 100 < 45 { 1 } else { 0 });
    }

    let mut work: Vec<i64> = vec![0; total as usize];
    let mut sink: i64 = 0;
    for _ in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % total) as usize;
        master[idx] = 1 - master[idx];
        work[..(total as usize)].copy_from_slice(&master[..(total as usize)]);
        sink += num_islands(&mut work, rows, cols);
    }
    println!("{}", sink);
}
