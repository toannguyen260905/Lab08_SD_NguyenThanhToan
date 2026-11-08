package A;

import java.util.EnumMap;
import A.Program6_16.Day;

public final class Commands6_16 {

    private Commands6_16() {
    }

    public static Command6_16 add(
            Program6_16 program, Show show, Day day) {

        final Show value = show.copy();

        return new Command6_16() {
            private Show previous;

            @Override
            public void execute() {
                previous = program.get(day);
                program.add(value, day);
            }

            @Override
            public void undo() {
                program.add(previous, day);
            }
        };
    }

    public static Command6_16 remove(Program6_16 program, Day day) {
        return new Command6_16() {
            private Show previous;

            @Override
            public void execute() {
                previous = program.get(day);
                program.remove(day);
            }

            @Override
            public void undo() {
                program.add(previous, day);
            }
        };
    }

    public static Command6_16 clear(Program6_16 program) {
        return new Command6_16() {
            private final EnumMap<Day, Show> previous =
                    new EnumMap<>(Day.class);

            @Override
            public void execute() {
                previous.clear();

                for (Day day : Day.values()) {
                    previous.put(day, program.get(day));
                }

                program.clear();
            }

            @Override
            public void undo() {
                for (Day day : Day.values()) {
                    program.add(previous.get(day), day);
                }
            }
        };
    }
}