// The Rust mirror of build_array.kara: a fresh String for every operation,
// as the Kara arm's to_string makes one.
fn build_array(target: &[i32], n: i32) -> Vec<String> {
    let mut ops: Vec<String> = Vec::new();
    let mut next = 0;
    for x in 1..=n {
        if next == target.len() {
            break;
        }
        ops.push("Push".to_string());
        if target[next] == x {
            next += 1;
        } else {
            ops.push("Pop".to_string());
        }
    }
    ops
}

fn main() {
    let mut seed: i64 = 1441;
    let mut targets: Vec<Vec<i32>> = Vec::new();
    for _ in 0..1000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let keep = 1 + seed / 65536 % 100;
        let mut target: Vec<i32> = Vec::new();
        for x in 1..=100 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            if seed / 65536 % 100 < keep {
                target.push(x);
            }
        }
        if target.is_empty() {
            target.push(100);
        }
        targets.push(target);
    }
    let mut check: i64 = 0;
    for _ in 0..200 {
        for target in targets.iter() {
            let ops = build_array(target, 100);
            let h = ops.iter().fold(0i64, |h, op| (h * 3 + if op == "Push" { 1 } else { 2 }) % 1000000007);
            check = (check * 131 + h) % 1000000007;
        }
    }
    println!("2 * 10^5 targets: checksum {}", check);
}
