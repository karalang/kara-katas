fn min_i64(a: i64, b: i64) -> i64 { if a < b { a } else { b } }
fn max_i64(a: i64, b: i64) -> i64 { if a > b { a } else { b } }
fn clamp0(x: i64) -> i64 { if x > 0 { x } else { 0 } }

fn compute_area(ax1: i64, ay1: i64, ax2: i64, ay2: i64,
                bx1: i64, by1: i64, bx2: i64, by2: i64) -> i64 {
    let area_a = (ax2 - ax1) * (ay2 - ay1);
    let area_b = (bx2 - bx1) * (by2 - by1);
    let overlap_w = clamp0(min_i64(ax2, bx2) - max_i64(ax1, bx1));
    let overlap_h = clamp0(min_i64(ay2, by2) - max_i64(ay1, by1));
    let overlap = overlap_w * overlap_h;
    area_a + area_b - overlap
}

fn main() {
    let pairs: i64 = 20000000;
    let mask: i64 = 16383;
    let modulus: i64 = 1000000007;
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..pairs {
        state = (state * 1103515245 + 12345) & 2147483647;
        let ax1 = state & mask;
        state = (state * 1103515245 + 12345) & 2147483647;
        let ax2 = ax1 + (state & mask);
        state = (state * 1103515245 + 12345) & 2147483647;
        let ay1 = state & mask;
        state = (state * 1103515245 + 12345) & 2147483647;
        let ay2 = ay1 + (state & mask);
        state = (state * 1103515245 + 12345) & 2147483647;
        let bx1 = state & mask;
        state = (state * 1103515245 + 12345) & 2147483647;
        let bx2 = bx1 + (state & mask);
        state = (state * 1103515245 + 12345) & 2147483647;
        let by1 = state & mask;
        state = (state * 1103515245 + 12345) & 2147483647;
        let by2 = by1 + (state & mask);
        let area = compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2);
        sink = (sink + area) % modulus;
    }
    println!("{}", sink);
}
