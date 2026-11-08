from pathlib import Path
import sys

root=Path(__file__).resolve().parents[1]
src=root/'src'/'A'
original=Path(r'C:\Users\Windows\Downloads\Concert\src\A')
def write(name,text): (src/(name+'.java')).write_text(text,encoding='utf-8')

if sys.argv[1]=='tests':
    write('ExerciseChecks','''package A;

final class ExerciseChecks {
    private ExerciseChecks() { }

    static void check(String expected, Object program, String step) {
        if (!expected.equals(program.toString())) {
            throw new AssertionError(step + "\\nExpected:\\n" + expected
                    + "Actual:\\n" + program);
        }
        System.out.println("PASS: " + step);
    }
}
''')
    for n in range(15,19):
        suffix=f'6_{n}'
        p='Program'+suffix
        cmd='Commands'+suffix
        cp='CommandProcessor'+suffix
        setup=f'{p} program = new {p}();\n'
        if n in [16,17]:setup+=f'        {cp} processor = new {cp}();\n'
        if n==15:
            setup+=f'''        Command6_15 add1 = {cmd}.add(program, movie1, Day.MONDAY);
        Command6_15 add2 = {cmd}.add(program, movie2, Day.TUESDAY);
        Command6_15 remove = {cmd}.remove(program, Day.MONDAY);
        Command6_15 clear = {cmd}.clear(program);
'''
        def action(op,args=''):
            if n==15:return {'add1':'add1.execute();','add2':'add2.execute();','remove':'remove.execute();','clear':'clear.execute();'}[op]
            method={'add1':f'add(movie1, Day.MONDAY)','add2':f'add(movie2, Day.TUESDAY)','remove':'remove(Day.MONDAY)','clear':'clear()'}[op]
            if n==18:return 'program.'+method+';'
            factory={'add1':'add(program, movie1, Day.MONDAY)','add2':'add(program, movie2, Day.TUESDAY)','remove':'remove(program, Day.MONDAY)','clear':'clear(program)'}[op]
            return f'processor.execute({cmd}.{factory});'
        text=f'''package A;

import A.{p}.Day;

/** Run this class as a Java Application for exercise 6.{n}. */
public class Main{suffix} {{
    public static void main(String[] args) {{
        Movie movie1 = new Movie("Movie 1", 2017, 120);
        Movie movie2 = new Movie("Movie 2", 2018, 130);
        {setup}
        String initial = program.toString();
        {action('add1')}
        String afterAdd1 = program.toString();
        {action('add2')}
        String afterAdd2 = program.toString();
        {action('remove')}
        String afterRemove = program.toString();
        {action('clear')}
        ExerciseChecks.check(initial, program, "clear");
'''
        target='program' if n==18 else 'processor'
        for name,expected in [('clear','afterRemove'),('remove','afterAdd2'),('add2','afterAdd1'),('add1','initial')]:
            undo=f'{name}.undo();' if n==15 else f'{target}.undoLast();'
            text+=f'        {undo}\n        ExerciseChecks.check({expected}, program, "undo {name}");\n'
        if n>=16:text+=f'        {target}.undoLast();\n        ExerciseChecks.check(initial, program, "empty undo");\n'
        if n>=17:
            for name,expected in [('add1','afterAdd1'),('add2','afterAdd2'),('remove','afterRemove'),('clear','initial')]:
                text+=f'        {target}.redoLast();\n        ExerciseChecks.check({expected}, program, "redo {name}");\n'
            text+=f'''        {target}.redoLast();
        ExerciseChecks.check(initial, program, "empty redo");
        {target}.undoLast();
'''
            branch='program.add(movie1, Day.WEDNESDAY);' if n==18 else f'processor.execute({cmd}.add(program, movie1, Day.WEDNESDAY));'
            text+=f'''        {branch}
        String branch = program.toString();
        {target}.redoLast();
        ExerciseChecks.check(branch, program, "new command clears redo");
'''
        # Verify overwriting an occupied day restores its previous show.
        if n==15:
            text+=f'''        program.add(movie1, Day.MONDAY);
        String beforeOverwrite = program.toString();
        Command6_15 overwrite = {cmd}.add(program, movie2, Day.MONDAY);
        overwrite.execute();
        overwrite.undo();
'''
        else:
            text+=f'        {action("add1")}\n        String beforeOverwrite = program.toString();\n'
            overwrite='program.add(movie2, Day.MONDAY);' if n==18 else f'processor.execute({cmd}.add(program, movie2, Day.MONDAY));'
            text+=f'        {overwrite}\n        {target}.undoLast();\n'
        text+=f'''        ExerciseChecks.check(beforeOverwrite, program, "undo overwrite");
        System.out.println("Completed exercise 6.{n}");
    }}
}}
'''
        write('Main'+suffix,text)
    sys.exit()

for name in ['Show','Movie','Concert','NullShow','Lab1']:
    write(name,(original/(name+'.java')).read_text(encoding='utf-8-sig'))
for n in range(15,19):
    suffix=f'6_{n}'
    p='Program'+suffix
    c='Command'+suffix
    cmd='Commands'+suffix
    cp='CommandProcessor'+suffix
    write(c,f'''package A;

public interface {c} {{
    void execute();
    void undo();
}}
''')
    program=(original/'Program.java').read_text().replace('Program',p)
    commands=(original/'Commands.java').read_text().replace('Commands',cmd).replace('Command',c).replace('Program',p)
    # Replace longest names first, avoiding replacing Command inside Commands twice.
    commands=(original/'Commands.java').read_text()
    import re
    commands=re.sub(r'\b(Commands|Command|Program)\b',lambda m:{'Commands':cmd,'Command':c,'Program':p}[m[0]],commands)
    if n==18:
        program=program.replace('    public '+p+'() {\n        clear();','    private final '+cp+' processor = new '+cp+'();\n\n    public '+p+'() {\n        clearDirect();')
        program=program.replace('public void clear()', 'void clearDirect()').replace('public void add(Show show, Day day)', 'void addDirect(Show show, Day day)').replace('public void remove(Day day)', 'void removeDirect(Day day)')
        insert=f'''    // Public operations record commands; direct operations only update data.
    public void add(Show show, Day day) {{
        Objects.requireNonNull(show);
        Objects.requireNonNull(day);
        processor.execute({cmd}.add(this, show, day));
    }}

    public void remove(Day day) {{
        Objects.requireNonNull(day);
        processor.execute({cmd}.remove(this, day));
    }}

    public void clear() {{
        processor.execute({cmd}.clear(this));
    }}

    public void undoLast() {{ processor.undoLast(); }}

    public void redoLast() {{ processor.redoLast(); }}

'''
        program=program.replace('    public Show get(Day day)',insert+'    public Show get(Day day)')
        commands=commands.replace('program.add(', 'program.addDirect(').replace('program.remove(', 'program.removeDirect(').replace('program.clear()', 'program.clearDirect()')
    write(p,program);write(cmd,commands)
    if n>=16:
        redoField=f'    private final Deque<{c}> redoStack = new ArrayDeque<>();\n' if n>=17 else ''
        clearRedo='        redoStack.clear();\n' if n>=17 else ''
        pushRedo='        redoStack.push(command);\n' if n>=17 else ''
        redo=f'''
    public void redoLast() {{
        if (redoStack.isEmpty()) return;
        {c} command = redoStack.peek();
        command.execute();
        redoStack.pop();
        undoStack.push(command);
    }}
''' if n>=17 else ''
        write(cp,f'''package A;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/** Owns command history; clients never access the stacks. */
public final class {cp} {{
    private final Deque<{c}> undoStack = new ArrayDeque<>();
{redoField}
    public void execute({c} command) {{
        Objects.requireNonNull(command);
        command.execute();
        undoStack.push(command);
{clearRedo}    }}

    public void undoLast() {{
        if (undoStack.isEmpty()) return;
        {c} command = undoStack.peek();
        command.undo();
        undoStack.pop();
{pushRedo}    }}
{redo}}}
''')
print('Created exercise sources in',src)
