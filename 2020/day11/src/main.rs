use std::fs::File;
use std::io::{self, BufRead, Error};

type AOCResult = std::result::Result<(), Error>;

#[derive(Clone, Eq, PartialEq, Debug)]
struct AOCPos {
    x: usize,
    y: usize,
}

type AOCPosState = char;

struct AOCProcessor {
    input: String,
    seating: Vec<Vec<char>>,
    result_a: usize,
    result_b: usize,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            seating: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.input) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.seating.clear();
    }

    pub fn finalize(&mut self) {
        let save_seating = self.seating.clone();
        self.finalize_a();
        self.seating = save_seating;
        self.finalize_b();
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            let row: Vec<char> = line.chars().map(|x| x).collect();
            self.seating.push(row);
        }
    }

    fn finalize_a(&mut self) {
        loop {
            if self.update_seating_a() == 0 {
                break;
            }
        }
        self.result_a = self.count_all_state('#');
        println!("result_a:{}", self.result_a);
    }

    fn finalize_b(&mut self) {
        loop {
            if self.update_seating_b() == 0 {
                break;
            }
        }
        self.result_b = self.count_all_state('#');
        println!("result_b:{}", self.result_b);
    }

    fn neighbours(&self, pos: &AOCPos) -> Vec<AOCPos> {
        let px = pos.x as i32;
        let py = pos.y as i32;
        let mut neighbours: Vec<AOCPos> = Vec::new();
        for y in &[py - 1, py, py + 1] {
            if *y < 0 || *y >= self.seating.len() as i32 {
                continue;
            }

            for x in &[px - 1, px, px + 1] {
                if *x < 0 || *x >= self.seating[pos.y].len() as i32 {
                    continue;
                }

                if *x != px || *y != py {
                    neighbours.push(AOCPos {
                        x: *x as usize,
                        y: *y as usize,
                    });
                }
            }
        }
        neighbours
    }

    fn count_all_state(&self, state: AOCPosState) -> usize {
        let mut n = 0;
        for y in 0..self.seating.len() {
            for x in 0..self.seating[y].len() {
                if self.seating[y][x] == state {
                    n += 1;
                }
            }
        }
        n
    }

    fn ray_neighbour_state(&self, sp: &AOCPos, np: &AOCPos) -> AOCPosState {
        let dx = (np.x as i32 - sp.x as i32).signum() as i32;
        let dy = (np.y as i32 - sp.y as i32).signum() as i32;
        let mut p = sp.clone();
        let mut state = '.';
        let maxy = self.seating.len() - 1;
        loop {
            if (dy < 0 && p.y == 0) || (dy > 0 && p.y >= maxy) {
                break;
            }
            p.y = (p.y as i32 + dy) as usize;

            let maxx = self.seating[p.y].len() - 1;
            if (dx < 0 && p.x == 0) || (dx > 0 && p.x >= maxx) {
                break;
            }
            p.x = (p.x as i32 + dx) as usize;

            state = self.seating[p.y][p.x];

            if state != '.' {
                break;
            }
        }
        state
    }

    fn count_ray_neighbour_state(
        &self,
        sp: &AOCPos,
        neighbours: &Vec<AOCPos>,
        state: AOCPosState,
    ) -> i32 {
        let mut count = 0;
        for n in neighbours {
            let ns = self.ray_neighbour_state(sp, n);
            if ns == state {
                count += 1;
            }
        }
        count
    }

    fn count_actual_neighbour_state(
        &self,
        _sp: &AOCPos,
        neighbours: &Vec<AOCPos>,
        state: AOCPosState,
    ) -> i32 {
        let mut n = 0;
        for p in neighbours {
            if self.seating[p.y][p.x] == state {
                n += 1;
            }
        }
        n
    }

    fn update_seating_a(&mut self) -> i32 {
        let mut n_seating_changes = 0;
        let mut new_seating: Vec<Vec<char>> = self.seating.clone();
        for y in 0..self.seating.len() {
            for x in 0..self.seating[y].len() {
                let old_state = self.seating[y][x];
                if old_state == '.' {
                    continue;
                }

                let p = AOCPos { x: x, y: y };
                let neighbours = self.neighbours(&p);
                let n_occupied = self.count_actual_neighbour_state(&p, &neighbours, '#');

                if old_state == 'L' && n_occupied == 0 {
                    new_seating[y][x] = '#';
                    n_seating_changes += 1;
                } else if old_state == '#' && n_occupied >= 4 {
                    new_seating[y][x] = 'L';
                    n_seating_changes += 1;
                }
            }
        }
        self.seating = new_seating;
        n_seating_changes
    }

    fn update_seating_b(&mut self) -> i32 {
        let mut n_seating_changes = 0;
        let mut new_seating: Vec<Vec<char>> = self.seating.clone();
        for y in 0..self.seating.len() {
            for x in 0..self.seating[y].len() {
                let old_state = self.seating[y][x];
                if old_state == '.' {
                    continue;
                }

                let p = AOCPos { x: x, y: y };

                let neighbours = self.neighbours(&p);
                let n_occupied = self.count_ray_neighbour_state(&p, &neighbours, '#');
                if old_state == 'L' && n_occupied == 0 {
                    new_seating[y][x] = '#';
                    n_seating_changes += 1;
                } else if old_state == '#' && n_occupied >= 5 {
                    new_seating[y][x] = 'L';
                    n_seating_changes += 1;
                }
            }
        }
        self.seating = new_seating;
        n_seating_changes
    }

}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
