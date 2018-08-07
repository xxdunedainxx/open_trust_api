
# App config table 
CREATE database open_trust_conf;
# Users table - user / admin / owner
CREATE TABLE user (
	user_id int NOT NULL AUTO_INCREMENT,
	when_created DATETIME,
	active int DEFAULT 1,
	role varchar(333),
	username varchar(333),
	password varchar(333),
	PRIMARY KEY(user_id)
)ENGINE=InnoDB;

INSERT INTO user (when_created, role, username,password) VALUES (now(), 'owner', 'open_trust_owner', 'OPENBLAH');

# Integration table (google / twilio)
CREATE TABLE integration(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(333),
    when_created DATETIME,
    active int DEFAULT 0, # integrations off by default 
    PRIMARY KEY(id)
)ENGINE=InnoDB;

INSERT INTO integration (name, when_created) VALUES ('gmail',now());
INSERT INTO integration (name, when_created) VALUES ('twilio',now());

CREATE database open_trust_app;
use open_trust_app;

# Service tables
CREATE TABLE service(
    service_id int NOT NULL AUTO_INCREMENT,
    name varchar(333),
    when_created DATETIME,
    description TEXT,
    active int DEFAULT 1,
    status int DEFAULT 1,
    PRIMARY KEY(service_id)
)ENGINE=InnoDB;

CREATE TABLE feature(
    feature_id int NOT NULL AUTO_INCREMENT,
    name varchar(333),
    when_created DATETIME,
    parent_service int NOT NULL,
    description TEXT,
    active int DEFAULT 1,
    status int DEFAULT 1,
    PRIMARY KEY(service_id)
)ENGINE=InnoDB;

CREATE TABLE status(
    status_id int NOT NULL AUTO_INCREMENT,
    name varchar(333),
    when_created DATETIME,
   	status_sprite varchar(333),
    PRIMARY KEY(status_id)
)ENGINE=InnoDB;

# Default states
INSERT INTO status (name,when_created,status_sprite) VALUES ('Online', now(), 'Online.png');
INSERT INTO status (name,when_created,status_sprite) VALUES ('Outage', now(), 'Outage.png');
INSERT INTO status (name,when_created,status_sprite) VALUES ('Maintanance', now(), 'Maintanance.png');

# Cron job tables

CREATE TABLE test_crons(
    cron_id int NOT NULL AUTO_INCREMENT,
    name varchar(333),
    when_created DATETIME,
    active int DEFAULT 1,
    number_of_retries int NOT NULL,
    type_of_frequency varchar(333), # weekly, yearly, monthly, minute, hour etc
    time_frequency varchar(333), # number times per week, which monthly, per minute, hour etc 
    # Ping, tcp, udp, custom selenium tests
    type_of_test varchar(333), 
    endpoint_to_test varchar(666),
    PRIMARY KEY(cron_id)
)ENGINE=InnoDB;

CREATE TABLE event (
    event_id int NOT NULL AUTO_INCREMENT,
    description TEXT,
    when_created DATETIME,
    active int DEFAULT 1,
    event_status int,
    impacted_componet varchar(333), # typically feature or service
    when_closed DATETIME,
    PRIMARY KEY(event_id)
)ENGINE=InnoDB;

CREATE TABLE event_comment(
    comment_id int NOT NULL AUTO_INCREMENT,
    comment TEXT,
    when_created DATETIME,
    event_id int NOT NULL,
    PRIMARY KEY(comment_id)
)ENGINE=InnoDB;

# Need table for event
# Need table for event comment