<?php

/**
 * API trait
 */

trait API {

    /**
     * Inform client that page should not be cached
     * @see https://stackoverflow.com/questions/13640109/how-to-prevent-browser-cache-for-php-site
     */
    function disable_cache() {
        if (! headers_sent()) {
            header('Expires: Sun, 01 Jan 2014 00:00:00 GMT');
            header('Cache-Control: no-store, no-cache, must-revalidate');
            header('Cache-Control: post-check=0, pre-check=0', FALSE);
            header('Pragma: no-cache');
        }
    }


    /**
     * Abort script and send HTTP error to client
     * @param int $status HTTP status code, e.g. 403
     * @param string $msg HTTP status message, e.g. "Forbidden"
     */
    function abort_with_error($status, $msg = "") {
        $h = trim('HTTP/1.1 ' . (int) $status . ' ' . $msg);
        if (headers_sent()) {
            echo '<h1>' . $h . '</h1>';
        } else {
            header($h);
            $this->disable_cache();
            $response = array(
                'status' => $status,
                'error' => $msg,
            );
            header("Content-Type: application/json");
            $json = json_encode($response, true);
            echo $json;
        }
        exit;
    }


    /**
     * Make sure that one of the specified HTTP methods is used.
     * Abort with error message if not.
     * @param string $methods string|array, e.g. "GET,POST" or array("GET", "POST")
     */
    public function restrict_http_method($methods) {
        if (! is_array($methods)) {
            $methods = explode(",", $methods);
        }

        $method_in_use = $_SERVER['REQUEST_METHOD'];
        foreach ($methods AS $method) {
            $method = str_replace(' ', '', $method);
            $method = trim($method);
            $method = strtoupper($method);
            if ($method == $method_in_use) {
                return true;
            }
        }
        $this->abort_with_error(405, "Method $method_in_use not allowed");
    }
    
    
    /**
     * Verify that all required fields are contained in the json body
     */
    public function verifyJsonContent($json, $requirements) {
        foreach ($requirements as $key) {
            if (!array_key_exists($key, $json)) {
                return false;
            }
        }
        return true;
    }
    

}


