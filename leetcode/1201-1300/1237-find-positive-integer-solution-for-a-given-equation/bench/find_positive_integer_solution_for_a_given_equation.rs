// LeetCode #1237 bench: the ★ arm in Rust, over the same 9 functions, z
// from 1 to 100 and 30 passes as the Kāra bench.

struct CustomFunction {
    id: i32,
}

impl CustomFunction {
    fn f(&self, x: i32, y: i32) -> i32 {
        match self.id {
            1 => x + y,
            2 => x * y,
            3 => x * x + y,
            4 => x + y * y,
            5 => x * x + y * y,
            6 => (x + y) * (x + y),
            7 => x * x * x + y * y * y,
            8 => x * x * y,
            _ => x * y * y,
        }
    }
}

fn find_solution(customfunction: &CustomFunction, z: i32) -> Vec<Vec<i32>> {
    let mut out = Vec::new();
    let (mut x, mut y) = (1, 1000);
    while x <= 1000 && y >= 1 {
        let v = customfunction.f(x, y);
        if v < z {
            x += 1;
        } else if v > z {
            y -= 1;
        } else {
            out.push(vec![x, y]);
            x += 1;
            y -= 1;
        }
    }
    out
}

fn main() {
    let mut check: i64 = 0;
    for _ in 0..30 {
        for id in 1..=9 {
            for z in 1..=100 {
                for p in find_solution(&CustomFunction { id }, z).iter() {
                    check = (check * 131 + p[0] as i64 * 1001 + p[1] as i64) % 1000000007;
                }
            }
        }
    }
    println!("9 functions, z from 1 to 100, 30 passes: checksum {check}");
}
