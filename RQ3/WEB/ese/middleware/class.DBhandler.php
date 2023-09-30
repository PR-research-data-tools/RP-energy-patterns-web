<?php

/**
 * Database handler
 */

// TODO: Change the following parameters according to your setup
class DBhandler {
    protected $db_servername = 'localhost';
    protected $db_username = 'username';
    protected $db_password = 'pa55w0rd';
    protected $db_dbname = 'energy_patterns';
    protected $mysqli;
    
    
    /**
     * Constructor
     */
    public function __construct() {
        // Create connection
        $this->mysqli = new mysqli($this->db_servername, $this->db_username, $this->db_password, $this->db_dbname);
        
        // Check connection
        if ($this->mysqli->connect_error) {
          die("Connection failed: " . $this->mysqli->connect_error);
        }
    }
    
    
    /**
     * Run a database query
     */
    public function query($q) {
        return $this->mysqli->query($q);
    }

}