package org.ese.testcases;

public interface TestCase {

    default void initWebDriver() {
        initWebDriver("chrome");
    }
    void initWebDriver(String browser);

    void run();
}
