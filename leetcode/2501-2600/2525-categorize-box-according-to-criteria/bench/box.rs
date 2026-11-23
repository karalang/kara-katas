// LeetCode #2525: Categorize Box According to Criteria -- Rust mirror of
// the benchmark (box.kara): the same boxes, passes, order and checksum.

fn categorize_box(length: i64, width: i64, height: i64, mass: i64) -> &'static str {
    let bulky = length >= 10000 || width >= 10000 || height >= 10000 || length * width * height >= 1000000000;
    let heavy = mass >= 100;
    match (bulky, heavy) {
        (true, true) => "Both",
        (true, false) => "Bulky",
        (false, true) => "Heavy",
        (false, false) => "Neither",
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2525;
    let mut boxes: Vec<(i64, i64, i64, i64)> = Vec::new();
    for t in 0..100000 {
        let top = if t % 2 == 0 { 100000 } else { 2000 };
        let length = wide_random(&mut seed) % top + 1;
        let width = wide_random(&mut seed) % top + 1;
        let height = wide_random(&mut seed) % top + 1;
        boxes.push((length, width, height, next_random(&mut seed) % 1000 + 1));
    }
    let passes = 220;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 100000;
        for i in 0..100000 {
            let (length, width, height, mass) = boxes[((start + i) % 100000) as usize];
            let name = categorize_box(length, width, height, mass);
            let code = if name == "Both" { 1 } else if name == "Bulky" { 2 } else if name == "Heavy" { 3 } else { 4 };
            check = (check * 31 + code + p) % 1000000007;
        }
    }
    println!("{passes} passes over 100000 boxes: checksum {check}");
}
