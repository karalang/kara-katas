fn kth_smallest(mat: Vec<Vec<i32>>, k: i32) -> i32 {
    let k = k as usize;
    let mut sums: Vec<i32> = vec![0];
    for row in mat.iter() {
        let mut next: Vec<i32> = Vec::new();
        for &s in sums.iter() {
            for &x in row.iter() {
                next.push(s + x);
            }
        }
        next.sort();
        next.truncate(k);
        sums = next;
    }
    sums[k - 1]
}

fn main() {
    let mut seed: i64 = 1439;
    let mut check: i64 = 0;
    for _ in 0..300 {
        let mut mat: Vec<Vec<i32>> = Vec::new();
        for _ in 0..40 {
            let mut row: Vec<i32> = Vec::new();
            for _ in 0..40 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                row.push((1 + seed / 65536 % 5000) as i32);
            }
            row.sort();
            mat.push(row);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = (1 + seed / 65536 % 200) as i32;
        check = (check * 131 + kth_smallest(mat, k) as i64) % 1000000007;
    }
    println!("300 matrices of 40 by 40: checksum {}", check);
}
