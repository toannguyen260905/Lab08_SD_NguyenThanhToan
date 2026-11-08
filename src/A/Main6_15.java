package A;

import A.Program6_15.Day;

/** Run this class as a Java Application for exercise 6.15. */
public class Main6_15 {
    public static void main(String[] args) {
        Movie movie1 = new Movie("Movie 1", 2017, 120);
        Movie movie2 = new Movie("Movie 2", 2018, 130);
        Program6_15 program = new Program6_15();
        Command6_15 add1 = Commands6_15.add(program, movie1, Day.MONDAY);
        Command6_15 add2 = Commands6_15.add(program, movie2, Day.TUESDAY);
        Command6_15 remove = Commands6_15.remove(program, Day.MONDAY);
        Command6_15 clear = Commands6_15.clear(program);

        String initial = program.toString();
        add1.execute();
        String afterAdd1 = program.toString();
        add2.execute();
        String afterAdd2 = program.toString();
        remove.execute();
        String afterRemove = program.toString();
        clear.execute();
        ExerciseChecks.check(initial, program, "clear");
        clear.undo();
        ExerciseChecks.check(afterRemove, program, "undo clear");
        remove.undo();
        ExerciseChecks.check(afterAdd2, program, "undo remove");
        add2.undo();
        ExerciseChecks.check(afterAdd1, program, "undo add2");
        add1.undo();
        ExerciseChecks.check(initial, program, "undo add1");
        program.add(movie1, Day.MONDAY);
        String beforeOverwrite = program.toString();
        Command6_15 overwrite = Commands6_15.add(program, movie2, Day.MONDAY);
        overwrite.execute();
        overwrite.undo();
        ExerciseChecks.check(beforeOverwrite, program, "undo overwrite");
        System.out.println("Completed exercise 6.15");
    }
}
