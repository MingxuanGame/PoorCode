package com.mx.haf.other;

import static com.mx.haf.HuntersAndFugitives.isStart;

public class GameTimer {
    public static void main() {
        isStart = true;
        LocationTimer.main();
        LocationTimer.thread.start();
    }
}
