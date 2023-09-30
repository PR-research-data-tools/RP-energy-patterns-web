package org.ese.testcases;

import org.ese.common.Navigator;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.safari.SafariDriver;

public class DynamicRetryDelay implements TestCase {

    // Define all parameters
    private WebDriver driver;
    private final int testVariant;
    private final String[] urls;
    private final int waitAfterLoading = 90000;
    private final Navigator navigator;

    private String websiteUrl = "";

    public DynamicRetryDelay(int variant, String[] urls) {
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

        // Quit session
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
