use std::fmt;

#[derive(Clone, Eq, PartialEq, Debug)]
pub enum AOCMachineOperation {
    INVALID,
    ACC,
    JMP,
    NOP,
}

#[derive(Clone, Debug)]
pub struct AOCMachineInstruction {
    operation: AOCMachineOperation,
    argument: i32,
}

pub type AOCMachineMemory = Vec<AOCMachineInstruction>;

#[derive(Clone, Debug)]
pub struct AOCMachineError;

#[allow(dead_code)]
pub type AOCMachineResult = std::result::Result<(), AOCMachineError>;

#[derive(Clone, Debug)]
pub struct AOCMachine {
    memory: AOCMachineMemory,
    program_counter: i32,
    accumulator: i32,
    pub jmp_v: Vec<i32>,
    pub nop_v: Vec<i32>,
}

impl AOCMachine {
    pub fn new() -> AOCMachine {
        AOCMachine {
            memory: Vec::new(),
            program_counter: 0,
            accumulator: 0,
            jmp_v: Vec::new(),
            nop_v: Vec::new(),
        }
    }

    pub fn reboot(&mut self) {
        self.memory.clear();
        self.jmp_v.clear();
        self.nop_v.clear();
        self.reset();
    }

    pub fn reset(&mut self) {
        self.program_counter = 0;
        self.accumulator = 0;
    }

    pub fn step(&mut self) -> AOCMachineResult {
        if self.program_counter < 0 || self.program_counter >= self.memory.len() as i32 {
            return Err(AOCMachineError);
        }

        let pc = self.program_counter;
        let instruction = self.memory.get(self.program_counter as usize).unwrap();

        match instruction.operation {
            AOCMachineOperation::NOP => {
                self.program_counter += 1;
            }
            AOCMachineOperation::ACC => {
                self.accumulator += instruction.argument;
                self.program_counter += 1;
            }
            AOCMachineOperation::JMP => {
                self.program_counter += instruction.argument;
            }
            _ => {}
        }

        println!(
            "pc:{}: instruction:{:?} -> pc:{}, accumulator:{}",
            pc, instruction, self.program_counter, self.accumulator
        );
        Ok(())
    }

    pub fn run(&mut self) -> bool {
        let mut seen_program_counters: Vec<bool> = vec![false; self.get_memory_usage()];
        let mut running = true;
        while running {
            let pc = self.get_program_counter();
            if pc < seen_program_counters.len() {
                if seen_program_counters[pc] {
                    running = false;
                } else {
                    seen_program_counters[pc] = true;
                    match self.step() {
                        Err(error) => {
                            panic!("{}", error);
                        }
                        _ => {}
                    }
                }
            } else {
                running = false;
            }
        }
        self.get_program_counter() >= self.get_memory_usage()
    }

    pub fn set_machine_operation(&mut self, pc: i32, operation: AOCMachineOperation) {
        let mut i = self.memory.get_mut(pc as usize).unwrap();
        i.operation = operation;
    }

    pub fn get_memory_usage(&self) -> usize {
        self.memory.len()
    }

    pub fn get_program_counter(&self) -> usize {
        self.program_counter as usize
    }

    pub fn get_accumulator(&self) -> i32 {
        self.accumulator
    }

    // pub fn get_instruction(&self, pc: usize) -> &AOCMachineInstruction {
    //     self.memory.get(pc).unwrap()
    // }

    pub fn load_instruction(&mut self, instruction: &str, argument: i32) -> AOCMachineResult {
        let operation = match instruction {
            "acc" => AOCMachineOperation::ACC,
            "nop" => AOCMachineOperation::NOP,
            "jmp" => AOCMachineOperation::JMP,
            _ => AOCMachineOperation::INVALID,
        };
        if operation == AOCMachineOperation::INVALID {
            return Err(AOCMachineError);
        }

        let instruction = AOCMachineInstruction {
            operation,
            argument,
        };
        match instruction.operation {
            AOCMachineOperation::NOP => {
                self.nop_v.push(self.memory.len() as i32);
            }
            AOCMachineOperation::JMP => {
                self.jmp_v.push(self.memory.len() as i32);
            }
            _ => {}
        }
        self.memory.push(instruction);
        Ok(())
    }
}

impl fmt::Display for AOCMachineError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Invalid Machine State")
    }
}
