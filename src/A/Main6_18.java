package A;

import A.Program6_18.Day;

/** Run this class as a Java Application for exercise 6.18. */
public class Main6_18 {
    public static void main(String[] args) {
        Movie movie1 = new Movie("Movie 1", 2017, 120);
        Movie movie2 = new Movie("Movie 2", 2018, 130);
        Program6_18 program = new Program6_18();

        String initial = program.toString();
        program.add(movie1, Day.MONDAY);
        String afterAdd1 = program.toString();
        program.add(movie2, Day.TUESDAY);
        String afterAdd2 = program.toString();
        program.remove(Day.MONDAY);
        String afterRemove = program.toString();
        program.clear();
        ExerciseChecks.check(initial, program, "clear");
        program.undoLast();
        ExerciseChecks.check(afterRemove, program, "undo clear");
        program.undoLast();
        ExerciseChecks.check(afterAdd2, program, "undo remove");
        program.undoLast();
        ExerciseChecks.check(afterAdd1, program, "undo add2");
        program.undoLast();
        ExerciseChecks.check(initial, program, "undo add1");
        program.undoLast();
        ExerciseChecks.check(initial, program, "empty undo");
        program.redoLast();
        ExerciseChecks.check(afterAdd1, program, "redo add1");
        program.redoLast();
        ExerciseChecks.check(afterAdd2, program, "redo add2");
        program.redoLast();
        ExerciseChecks.check(afterRemove, program, "redo remove");
        program.redoLast();
        ExerciseChecks.check(initial, program, "redo clear");
        program.redoLast();
        ExerciseChecks.check(initial, program, "empty redo");
        program.undoLast();
        program.add(movie1, Day.WEDNESDAY);
        String branch = program.toString();
        program.redoLast();
        ExerciseChecks.check(branch, program, "new command clears redo");
        program.add(movie1, Day.MONDAY);
        String beforeOverwrite = program.toString();
        program.add(movie2, Day.MONDAY);
        program.undoLast();
        ExerciseChecks.check(beforeOverwrite, program, "undo overwrite");
        System.out.println("Completed exercise 6.18");
    }
}
