package A;

import java.util.EnumMap;
import A.Program6_18.Day;

public final class Commands6_18 {

    private Commands6_18() {
    }

    public static Command6_18 add(
            Program6_18 program, Show show, Day day) {

        final Show value = show.copy();

        return new Command6_18() {
            private Show previous;

            @Override
            public void execute() {
                previous = program.get(day);
                program.addDirect(value, day);
            }

            @Override
            public void undo() {
                program.addDirect(previous, day);
            }
        };
    }

    public static Command6_18 remove(Program6_18 program, Day day) {
        return new Command6_18() {
            private Show previous;

            @Override
            public void execute() {
                previous = program.get(day);
                program.removeDirect(day);
            }

            @Override
            public void undo() {
                program.addDirect(previous, day);
            }
        };
    }

    public static Command6_18 clear(Program6_18 program) {
        return new Command6_18() {
            private final EnumMap<Day, Show> previous =
                    new EnumMap<>(Day.class);

            @Override
            public void execute() {
                previous.clear();

                for (Day day : Day.values()) {
                    previous.put(day, program.get(day));
                }

                program.clearDirect();
            }

            @Override
            public void undo() {
                for (Day day : Day.values()) {
                    program.addDirect(previous.get(day), day);
                }
            }
        };
    }
}