package org.ese;

import org.ese.common.PropertyReader;
import org.ese.testcases.*;

public class Main {

    /**
     * Usage to run test case with specific variant:
     * java -cp "target/classes:target/dependency/*" org.ese.Main [testcase:String] [variant:Integer]
     *
     * @param args
     */
    public static void main(String[] args) {
        // Check number of arguments
        if (args.length < 2) {
            System.out.println("Proper Usage is: java -cp \"target/classes:target/dependency/*\" org.ese.Main [testcase:String] [variant:Integer]");
            System.exit(0);
        }

        String testcaseArg = args[0];
        int variantArg = 0;

        // Verify that second argument is an integer
        try {
            variantArg = Integer.parseInt(args[1]);
        } catch (Exception e) {
            System.out.println("variant must be an integer");
            System.exit(0);
        }

        // Read properties
        PropertyReader properties = new PropertyReader();
        String[] urls = properties.readProperties(testcaseArg);

        // Run test case
        TestCase testCase = null;
        switch (testcaseArg) {
            case "lazyLoading":
                System.out.printf("Running test case 'Lazy Loading', variant %s\n", variantArg);
                testCase = new LazyLoading(variantArg, urls);
                break;
            case "dynamicRetryDelay":
                System.out.printf("Running test case 'Dynamic Retry Delay', variant %s\n", variantArg);
                testCase = new DynamicRetryDelay(variantArg, urls);
                break;
            default:
                System.out.printf("Unknown test case: %s!", testcaseArg);
                System.exit(0);
        }

        testCase.initWebDriver();
        testCase.run();
    }

}
