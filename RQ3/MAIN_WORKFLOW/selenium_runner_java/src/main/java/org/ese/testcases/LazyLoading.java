package org.ese.testcases;

import org.ese.common.Navigator;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.safari.SafariDriver;

public class LazyLoading implements TestCase {

    // Define all parameters
    private WebDriver driver;
    private final int testVariant;
    private final String[] urls;
    private final int scroll_delta_y = 37;
    private final int scrollRepetitions = 384;
    private final int waitAfterLoading = 5000;
    private final int waitAfterScrolling = 100;
    private final int waitBeforeQuit = 3000;
    private final Navigator navigator;

    private JavascriptExecutor js;
    private String websiteUrl = "";

    public LazyLoading(int variant, String[] urls) {
        this.urls = urls;
        this.navigator = new Navigator();
        if (variant < 0 || variant > 2 * urls.length) {
            this.testVariant = 0;
        }
        else {
            this.testVariant = variant;
        }
        this.websiteUrl = this.urls[this.testVariant % urls.length];
    }

    @Override
    public void run() {
        // Navigate to Webpage and wait
        driver.get(websiteUrl);
        navigator.pause(waitAfterLoading);

        // Prepare for interaction
        js = (JavascriptExecutor) driver;

        // Scroll up and down
        for (int s = 0; s < scrollRepetitions; s++) {
            js.executeScript(String.format("window.scrollBy(0, %d)", scroll_delta_y));
            navigator.pause(waitAfterScrolling);
        }

        // Quit session
        navigator.pause(waitBeforeQuit);
        driver.quit();
    }

    @Override
    public void initWebDriver() {
        if (this.testVariant >= this.urls.length) {
            this.initWebDriver("safari");
        }
        else {
            this.initWebDriver("chrome");
        }
    }

    @Override
    public void initWebDriver(String browser) {
        // Add option to start in incognito mode
        ChromeOptions option = new ChromeOptions();
        option.addArguments("incognito");

        // Start Selenium Browser
        switch (browser) {
            case "safari":
                this.driver = new SafariDriver();
                break;
            case "chrome":
                this.driver = new ChromeDriver(option);
                break;
            default:
                System.out.printf("Unknown browser %s\n", browser);
                System.exit(0);
        }
        driver.manage().window().maximize();
    }

}
