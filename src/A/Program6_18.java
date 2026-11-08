package A;

import java.util.EnumMap;
import java.util.Objects;

public final class Program6_18 {

    public enum Day {
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
        FRIDAY, SATURDAY, SUNDAY
    }

    private final EnumMap<Day, Show> shows =
            new EnumMap<>(Day.class);

    private final CommandProcessor6_18 processor = new CommandProcessor6_18();

    public Program6_18() {
        clearDirect();
    }

    void clearDirect() {
        for (Day day : Day.values()) {
            shows.put(day, new NullShow());
        }
    }

    void addDirect(Show show, Day day) {
        Objects.requireNonNull(show);
        Objects.requireNonNull(day);
        shows.put(day, show.copy());
    }

    void removeDirect(Day day) {
        Objects.requireNonNull(day);
        shows.put(day, new NullShow());
    }

    // Public operations record commands; direct operations only update data.
    public void add(Show show, Day day) {
        Objects.requireNonNull(show);
        Objects.requireNonNull(day);
        processor.execute(Commands6_18.add(this, show, day));
    }

    public void remove(Day day) {
        Objects.requireNonNull(day);
        processor.execute(Commands6_18.remove(this, day));
    }

    public void clear() {
        processor.execute(Commands6_18.clear(this));
    }

    public void undoLast() { processor.undoLast(); }

    public void redoLast() { processor.redoLast(); }

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