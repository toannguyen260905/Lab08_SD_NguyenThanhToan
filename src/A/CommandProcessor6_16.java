package A;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/** Owns command history; clients never access the stacks. */
public final class CommandProcessor6_16 {
    private final Deque<Command6_16> undoStack = new ArrayDeque<>();

    public void execute(Command6_16 command) {
        Objects.requireNonNull(command);
        command.execute();
        undoStack.push(command);
    }

    public void undoLast() {
        if (undoStack.isEmpty()) return;
        Command6_16 command = undoStack.peek();
        command.undo();
        undoStack.pop();
    }
}
