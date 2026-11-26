fn find_diagonal_order(nums: &[Vec<i32>]) -> Vec<i32> {
    let mut diagonals: Vec<Vec<i32>> = Vec::new();
    for i in (0..nums.len()).rev() {
        for j in 0..nums[i].len() {
            while diagonals.len() <= i + j {
                diagonals.push(Vec::new());
            }
            diagonals[i + j].push(nums[i][j]);
        }
    }
    let mut order: Vec<i32> = Vec::new();
    for d in diagonals.iter() {
        order.extend(d.iter());
    }
    order
}

fn main() {
    let mut seed: i64 = 1424;
    let mut pool: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let n = 1 + seed / 65536 % 9;
        let mut row: Vec<i32> = Vec::new();
        for _ in 0..n {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            row.push((1 + seed / 65536 % 100000) as i32);
        }
        pool.push(row);
    }
    let mut check: i64 = 0;
    for _ in 0..300 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % 80001) as usize;
        for &x in find_diagonal_order(&pool[start..start + 20000]).iter() {
            check = (check * 131 + x as i64) % 1000000007;
        }
    }
    println!("300 windows of 2 * 10^4 rows: checksum {}", check);
}
