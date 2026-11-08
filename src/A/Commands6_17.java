package A;

import java.util.EnumMap;
import A.Program6_17.Day;

public final class Commands6_17 {

    private Commands6_17() {
    }

    public static Command6_17 add(
            Program6_17 program, Show show, Day day) {

        final Show value = show.copy();

        return new Command6_17() {
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

    public static Command6_17 remove(Program6_17 program, Day day) {
        return new Command6_17() {
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

    public static Command6_17 clear(Program6_17 program) {
        return new Command6_17() {
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