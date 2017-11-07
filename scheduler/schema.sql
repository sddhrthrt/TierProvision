CREATE TABLE task {
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'name' VARCHAR(128) NOT NULL,
    'rtt' INT,
    'def' VARCHAR(1024)
}
CREATE TABLE task_request {
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'task_id' INT NOT NULL, 
    'resources' VARCHAR(128),
    'rtt' INT,
    'stats' VARCHAR(1024),
    FOREIGN_KEY (task_id) references task(id)
}
CREATE TABLE node {
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'resources' VARCHAR(128),
    'rtt' INT,
    'stats' VARCHAR(1024)
}
CREATE TABLE task_stats {
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'task_id' INT NOT NULL,
    ''
}