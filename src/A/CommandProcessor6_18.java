package A;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/** Owns command history; clients never access the stacks. */
public final class CommandProcessor6_18 {
    private final Deque<Command6_18> undoStack = new ArrayDeque<>();
    private final Deque<Command6_18> redoStack = new ArrayDeque<>();

    public void execute(Command6_18 command) {
        Objects.requireNonNull(command);
        command.execute();
        undoStack.push(command);
        redoStack.clear();
    }

    public void undoLast() {
        if (undoStack.isEmpty()) return;
        Command6_18 command = undoStack.peek();
        command.undo();
        undoStack.pop();
        redoStack.push(command);
    }

    public void redoLast() {
        if (redoStack.isEmpty()) return;
        Command6_18 command = redoStack.peek();
        command.execute();
        redoStack.pop();
        undoStack.push(command);
    }
}
