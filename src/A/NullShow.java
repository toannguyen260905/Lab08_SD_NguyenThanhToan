package A;

public final class NullShow implements Show {

    @Override
    public String description() {
        return "Khong co show";
    }

    @Override
    public int runningTime() {
        return 0;
    }

    @Override
    public Show copy() {
        return new NullShow();
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof NullShow;
    }

    @Override
    public int hashCode() {
        return NullShow.class.hashCode();
    }
}