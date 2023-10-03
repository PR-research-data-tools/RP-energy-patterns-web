package org.ese.common;

import org.ese.Main;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class PropertyReader {

    public String[] readProperties(String testcase) {

        // Read properties file
        Properties testUrls = new Properties();
        try {
            InputStream inputStream = Main.class.getClassLoader().getResourceAsStream("resources/websites.xml");
            testUrls.loadFromXML(inputStream);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // Verify if key for provided test case exists and read number of variants
        if (!testUrls.containsKey(testcase)) {
            System.out.printf("Test case is missing in websites.xml properties file: %s!", testcase);
            System.exit(0);
        }

        // Key exists => Try to read number of variants
        int numVariants = 0;
        try {
            numVariants = Integer.parseInt(testUrls.getProperty(testcase));
        } catch (Exception e) {
            System.out.println("Value for number of test websites in properties file must be an integer");
            System.exit(0);
        }

        // Read urls for provided test case
        String[] urls = new String[numVariants];
        for (int var = 0; var < numVariants; var++) {
            String key = testcase + ".url." + var;
            if (testUrls.containsKey(key)) {
                urls[var] = testUrls.getProperty(key);
                System.out.println("Url for " + testcase + "." + var + ": " + urls[var]);
            }
            else {
                System.out.println("No url for " + key + " provided in properties file!");
                System.exit(0);
            }
        }

        return urls;
    }
}
