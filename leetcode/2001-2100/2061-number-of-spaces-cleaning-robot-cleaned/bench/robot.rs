// LeetCode #2061: Number of Spaces Cleaning Robot Cleaned -- Rust mirror of
// the ★ arm's benchmark (robot.kara): 600 spiral rooms of 200 to 300 by
// 200 to 300, the robot walked one move at a time, states and cells kept
// in flat `Vec<bool>`s.

const DR: [i64; 4] = [0, 1, 0, -1];
const DC: [i64; 4] = [1, 0, -1, 0];

fn number_of_clean_rooms(room: &[Vec<i64>]) -> i64 {
    let (m, n) = (room.len() as i64, room[0].len() as i64);
    let mut seen = vec![false; (m * n * 4) as usize];
    let mut cleaned = vec![false; (m * n) as usize];
    let mut count = 0;
    let (mut r, mut c, mut d) = (0i64, 0i64, 0i64);
    while !seen[((r * n + c) * 4 + d) as usize] {
        seen[((r * n + c) * 4 + d) as usize] = true;
        if !cleaned[(r * n + c) as usize] {
            cleaned[(r * n + c) as usize] = true;
            count += 1;
        }
        let (nr, nc) = (r + DR[d as usize], c + DC[d as usize]);
        if nr >= 0 && nr < m && nc >= 0 && nc < n && room[nr as usize][nc as usize] == 0 {
            r = nr;
            c = nc;
        } else {
            d = (d + 1) % 4;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn spiral(m: usize, n: usize) -> Vec<Vec<i64>> {
    let mut room = vec![vec![0i64; n]; m];
    let (mut top, mut left, mut bottom, mut right) = (0usize, 0usize, m - 1, n - 1);
    loop {
        if top + 2 > bottom {
            break;
        }
        room[top + 1][left] = 1;
        top += 2;
        if left + 2 > right {
            break;
        }
        room[top][right - 1] = 1;
        right -= 2;
        if bottom < top + 2 {
            break;
        }
        room[bottom - 1][right] = 1;
        bottom -= 2;
        if right < left + 2 {
            break;
        }
        room[bottom][left + 1] = 1;
        left += 2;
    }
    room
}

fn main() {
    let mut seed = 2061i64;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..600 {
        let m = (next_random(&mut seed) % 101 + 200) as usize;
        let n = (next_random(&mut seed) % 101 + 200) as usize;
        let a = number_of_clean_rooms(&spiral(m, n));
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("600 rooms: {} cleaned, checksum {}", total, check);
}
