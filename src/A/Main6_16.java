package A;

import A.Program6_16.Day;

/** Run this class as a Java Application for exercise 6.16. */
public class Main6_16 {
    public static void main(String[] args) {
        Movie movie1 = new Movie("Movie 1", 2017, 120);
        Movie movie2 = new Movie("Movie 2", 2018, 130);
        Program6_16 program = new Program6_16();
        CommandProcessor6_16 processor = new CommandProcessor6_16();

        String initial = program.toString();
        processor.execute(Commands6_16.add(program, movie1, Day.MONDAY));
        String afterAdd1 = program.toString();
        processor.execute(Commands6_16.add(program, movie2, Day.TUESDAY));
        String afterAdd2 = program.toString();
        processor.execute(Commands6_16.remove(program, Day.MONDAY));
        String afterRemove = program.toString();
        processor.execute(Commands6_16.clear(program));
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
        processor.execute(Commands6_16.add(program, movie1, Day.MONDAY));
        String beforeOverwrite = program.toString();
        processor.execute(Commands6_16.add(program, movie2, Day.MONDAY));
        processor.undoLast();
        ExerciseChecks.check(beforeOverwrite, program, "undo overwrite");
        System.out.println("Completed exercise 6.16");
    }
}
