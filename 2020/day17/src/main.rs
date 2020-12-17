use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

#[derive(Copy, Clone, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
struct AOCPoint {
    pub x: i32,
    pub y: i32,
    pub z: i32,
    pub w: i32,
}

impl AOCPoint {
    pub fn new(x: i32, y: i32, z: i32, w: i32) -> Self {
        AOCPoint {
            x: x,
            y: y,
            z: z,
            w: w,
        }
    }
    pub fn neighbours(&self, with_w: bool) -> Vec<AOCPoint> {
        let mut neighbours: Vec<AOCPoint> = Vec::new();
        for dx in [-1, 0, 1].iter() {
            for dy in [-1, 0, 1].iter() {
                for dz in [-1, 0, 1].iter() {
                    if with_w {
                        for dw in [-1, 0, 1].iter() {
                            if *dx != 0 || *dy != 0 || *dz != 0 || *dw != 0 {
                                neighbours.push(AOCPoint::new(
                                    self.x + dx,
                                    self.y + dy,
                                    self.z + dz,
                                    self.w + dw,
                                ));
                            }
                        }
                    } else {
                        if *dx != 0 || *dy != 0 || *dz != 0 {
                            neighbours.push(AOCPoint::new(
                                self.x + dx,
                                self.y + dy,
                                self.z + dz,
                                self.w,
                            ));
                        }
                    }
                }
            }
        }
        neighbours
    }
}

struct AOCProcessor {
    source: String,
    cells: HashSet<AOCPoint>,
    generation: u64,
}

impl AOCProcessor {
    pub fn new(source: String) -> AOCProcessor {
        AOCProcessor {
            source,
            cells: HashSet::new(),
            generation: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();
        let _ = match File::open(&self.source) {
            Ok(file) => {
                let mut lineno: i32 = 0;
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..], lineno);
                        lineno += 1;
                    }
                }
            }
            Err(error) => return Err(error),
        };
        self.finalize();

        Ok(())
    }

    fn initialize(&mut self) {
        self.cells.clear();
        self.generation = 0;
    }

    fn finalize(&mut self) {
        let save_cells = self.cells.clone();
        let save_generation = self.generation;
        let result_a = self.finalize_a();

        self.cells = save_cells;
        self.generation = save_generation;
        let result_b = self.finalize_b();
        println!("result_a:{}", result_a);
        println!("result_b:{}", result_b);
    }

    fn finalize_a(&mut self) -> usize {
        if AOCDEBUG {
            self.print_cube(false);
        }
        while self.generation < 6 {
            self.step(false);
            self.generation += 1;
            if AOCDEBUG {
                println!("generation:{}", self.generation);
                self.print_cube(false);
                println!("population:{}", self.cells.len());
            }
        }
        self.cells.len()
    }

    fn finalize_b(&mut self) -> usize {
        if AOCDEBUG {
            self.print_cube(true);
        }
        while self.generation < 6 {
            self.step(true);
            self.generation += 1;
            if AOCDEBUG {
                println!("generation:{}", self.generation);
                self.print_cube(true);
                println!("population:{}", self.cells.len());
            }
        }
        self.cells.len()
    }

    fn step(&mut self, with_w: bool) {
        let mut eval_cells: HashSet<AOCPoint> = HashSet::new();
        let mut new_live_cells: HashSet<AOCPoint> = HashSet::new();

        // collect the cells to evaluate
        for p in self.cells.clone() {
            if !eval_cells.contains(&p) {
                eval_cells.insert(p);
            }
            for n in p.neighbours(with_w) {
                if !eval_cells.contains(&n) {
                    eval_cells.insert(n);
                }
            }
        }

        // iteratre through them and decide new population
        for p in eval_cells {
            let mut live_count = 0;
            for n in p.neighbours(with_w) {
                if self.cells.contains(&n) {
                    live_count += 1;
                }
            }
            if self.cells.contains(&p) {
                if live_count >= 2 && live_count <= 3 {
                    new_live_cells.insert(p);
                }
            } else {
                if live_count == 3 {
                    new_live_cells.insert(p);
                }
            }
        }
        self.cells = new_live_cells;
    }

    fn min_point(&self) -> AOCPoint {
        AOCPoint::new(
            match self.cells.iter().map(|p| p.x).min() {
                Some(x) => x,
                None => 0,
            },
            match self.cells.iter().map(|p| p.y).min() {
                Some(y) => y,
                None => 0,
            },
            match self.cells.iter().map(|p| p.z).min() {
                Some(z) => z,
                None => 0,
            },
            match self.cells.iter().map(|p| p.w).min() {
                Some(w) => w,
                None => 0,
            },
        )
    }

    fn max_point(&self) -> AOCPoint {
        AOCPoint::new(
            match self.cells.iter().map(|p| p.x).max() {
                Some(x) => x,
                None => 0,
            },
            match self.cells.iter().map(|p| p.y).max() {
                Some(y) => y,
                None => 0,
            },
            match self.cells.iter().map(|p| p.z).max() {
                Some(z) => z,
                None => 0,
            },
            match self.cells.iter().map(|p| p.w).max() {
                Some(w) => w,
                None => 0,
            },
        )
    }

    fn print_cube(&self, with_w: bool) {
        let min_p = self.min_point();
        let max_p = self.max_point();

        println!("{:?} - {:?}", self.min_point(), self.max_point());
        for w in min_p.w..max_p.w + 1 {
            for z in min_p.z..max_p.z + 1 {
                if with_w {
                    println!("z={}, w={}", z, w);
                } else {
                    println!("z={}", z);
                }
                for y in min_p.y..max_p.y + 1 {
                    let mut line: String = String::from("");
                    for x in min_p.x..max_p.x + 1 {
                        let p = AOCPoint::new(x, y, z, w);
                        line = line
                            + match self.cells.contains(&p) {
                                true => "#",
                                false => ".",
                            };
                    }
                    println!("{}", line);
                }
            }
        }
    }

    fn process_line(&mut self, line: &str, lineno: i32) {
        if line.len() > 0 {
            println!("input[{}]:{}", lineno, line);
            let mut x = 0;
            for c in line.chars() {
                let state = match c {
                    '#' => true,
                    _ => false,
                };
                if state {
                    let p = AOCPoint::new(x, lineno, 0, 0);
                    self.cells.insert(p);
                }
                x += 1;
            }
        }
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
