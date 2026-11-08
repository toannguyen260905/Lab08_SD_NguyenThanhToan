package A;

import java.util.EnumMap;
import java.util.Objects;

public final class Program6_16 {

    public enum Day {
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
        FRIDAY, SATURDAY, SUNDAY
    }

    private final EnumMap<Day, Show> shows =
            new EnumMap<>(Day.class);

    public Program6_16() {
        clear();
    }

    public void clear() {
        for (Day day : Day.values()) {
            shows.put(day, new NullShow());
        }
    }

    public void add(Show show, Day day) {
        Objects.requireNonNull(show);
        Objects.requireNonNull(day);
        shows.put(day, show.copy());
    }

    public void remove(Day day) {
        Objects.requireNonNull(day);
        shows.put(day, new NullShow());
    }

    public Show get(Day day) {
        Objects.requireNonNull(day);
        return shows.get(day).copy();
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();

        for (Day day : Day.values()) {
            result.append(day)
                  .append(": ")
                  .append(shows.get(day).description())
                  .append(System.lineSeparator());
        }

        return result.toString();
    }
}