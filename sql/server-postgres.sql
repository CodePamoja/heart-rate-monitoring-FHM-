CREATE TABLE maternal_information (
	maternal_ID SERIAL PRIMARY KEY,
	uuid TEXT UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	date_of_birth DATE NOT NULL,
	phone_number TEXT UNIQUE,
	id_number TEXT UNIQUE,
	client_created TEXT,
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pregnancy_information (
	pregnancy_ID SERIAL PRIMARY KEY,
	maternal_uuid TEXT NOT NULL,
	location TEXT NOT NULL,
	pregnancy_type TEXT DEFAULT 'single',
	expected_delivery_date DATE NOT NULL,
	pregnancy_count TEXT NOT NULL,
	FOREIGN KEY (maternal_uuid) REFERENCES maternal_information(uuid) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE monitor_readings (
	hrm_data_ID SERIAL PRIMARY KEY,
	uuid TEXT UNIQUE NOT NULL,
	phone_number TEXT,
	id_number TEXT,
	device_id TEXT,
	height REAL,
	weight REAL,
	temperature REAL,
	heart_rate REAL,
	fetal_heart_rate REAL,
	client_created TEXT,
	data_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);