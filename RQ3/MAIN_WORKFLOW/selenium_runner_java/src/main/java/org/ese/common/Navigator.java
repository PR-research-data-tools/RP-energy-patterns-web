package org.ese.common;

public class Navigator {

    public Navigator() {
    }

    public void pause(int duration) {
        try {
            Thread.sleep(duration);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

}
