// Benchmark for #858: Mirror Reflection -- Rust twin of the Kāra trace arm
// (the ray traced from wall to wall), in every room LeetCode allows.

fn mirror_reflection(p: i64, q: i64) -> i64 {
    let mut y = 0;
    let mut up = true;
    let mut east = false;
    loop {
        if up {
            y += q;
            if y > p {
                y = 2 * p - y;
                up = false;
            }
        } else {
            y -= q;
            if y < 0 {
                y = -y;
                up = true;
            }
        }
        east = !east;
        if y == p {
            return if east { 1 } else { 2 };
        }
        // the south-west corner is never reached, so this is the east wall
        if y == 0 {
            return 0;
        }
    }
}

fn main() {
    let mut counts = [0i64; 3];
    let mut check: i64 = 0;
    for p in 1..=1000i64 {
        for q in 1..=p {
            let r = mirror_reflection(p, q);
            counts[r as usize] += 1;
            check = (check * 3 + r) % 1000000007;
        }
    }
    println!(
        "500500 rooms: receptor 0 {} times, 1 {}, 2 {}, checksum {}",
        counts[0], counts[1], counts[2], check
    );
}
