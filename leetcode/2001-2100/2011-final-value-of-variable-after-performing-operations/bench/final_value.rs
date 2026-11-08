// LeetCode #2011: Final Value of Variable After Performing Operations -- the
// ★ arm's benchmark, a mirror of final_value.kara.

fn final_value_after_operations(operations: &[String]) -> i64 {
    let mut x = 0;
    for op in operations {
        match op.as_str() {
            "++X" | "X++" => x += 1,
            "--X" | "X--" => x -= 1,
            _ => {}
        }
    }
    x
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let forms = ["++X", "X++", "--X", "X--"];
    let mut seed = 2011i64;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..20000 {
        let up = next_random(&mut seed) % 11;
        let mut operations = Vec::new();
        for _ in 0..100 {
            let down = if next_random(&mut seed) % 10 < up { 0 } else { 2 };
            operations.push(forms[(down + next_random(&mut seed) % 2) as usize].to_string());
        }
        lists.push(operations);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for operations in &lists {
            let answer = final_value_after_operations(operations);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer + 100) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
