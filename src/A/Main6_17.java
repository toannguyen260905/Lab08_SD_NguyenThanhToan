package A;

import A.Program6_17.Day;

/** Run this class as a Java Application for exercise 6.17. */
public class Main6_17 {
    public static void main(String[] args) {
        Movie movie1 = new Movie("Movie 1", 2017, 120);
        Movie movie2 = new Movie("Movie 2", 2018, 130);
        Program6_17 program = new Program6_17();
        CommandProcessor6_17 processor = new CommandProcessor6_17();

        String initial = program.toString();
        processor.execute(Commands6_17.add(program, movie1, Day.MONDAY));
        String afterAdd1 = program.toString();
        processor.execute(Commands6_17.add(program, movie2, Day.TUESDAY));
        String afterAdd2 = program.toString();
        processor.execute(Commands6_17.remove(program, Day.MONDAY));
        String afterRemove = program.toString();
        processor.execute(Commands6_17.clear(program));
        ExerciseChecks.check(initial, program, "clear");
        processor.undoLast();
        ExerciseChecks.check(afterRemove, program, "undo clear");
        processor.undoLast();
        ExerciseChecks.check(afterAdd2, program, "undo remove");
        processor.undoLast();
        ExerciseChecks.check(afterAdd1, program, "undo add2");
        processor.undoLast();
        ExerciseChecks.check(initial, program, "undo add1");
        processor.undoLast();
        ExerciseChecks.check(initial, program, "empty undo");
        processor.redoLast();
        ExerciseChecks.check(afterAdd1, program, "redo add1");
        processor.redoLast();
        ExerciseChecks.check(afterAdd2, program, "redo add2");
        processor.redoLast();
        ExerciseChecks.check(afterRemove, program, "redo remove");
        processor.redoLast();
        ExerciseChecks.check(initial, program, "redo clear");
        processor.redoLast();
        ExerciseChecks.check(initial, program, "empty redo");
        processor.undoLast();
        processor.execute(Commands6_17.add(program, movie1, Day.WEDNESDAY));
        String branch = program.toString();
        processor.redoLast();
        ExerciseChecks.check(branch, program, "new command clears redo");
        processor.execute(Commands6_17.add(program, movie1, Day.MONDAY));
        String beforeOverwrite = program.toString();
        processor.execute(Commands6_17.add(program, movie2, Day.MONDAY));
        processor.undoLast();
        ExerciseChecks.check(beforeOverwrite, program, "undo overwrite");
        System.out.println("Completed exercise 6.17");
    }
}
