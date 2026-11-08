package A;

final class ExerciseChecks {
    private ExerciseChecks() { }

    static void check(String expected, Object program, String step) {
        if (!expected.equals(program.toString())) {
            throw new AssertionError(step + "\nExpected:\n" + expected
                    + "Actual:\n" + program);
        }
        System.out.println("PASS: " + step);
    }
}
