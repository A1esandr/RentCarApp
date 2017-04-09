CREATE DATABASE rentdb CHARACTER SET utf8 COLLATE utf8_general_ci;

use rentdb;

CREATE TABLE brand ( 
	brand_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	brand_name VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE auto ( 
	auto_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	brand_id INT,
	auto_number VARCHAR(10),
  	FOREIGN KEY (brand_id)
  	REFERENCES brand(brand_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE place ( 
	place_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	place_name VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE rent ( 
	rent_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	auto_id INT,
	renter VARCHAR(100),
	place_start INT,
	place_finish INT,
	rent_beg_date DATE DEFAULT NULL,
	rent_end_date DATE DEFAULT NULL,

  	FOREIGN KEY (auto_id)
  	REFERENCES auto(auto_id),

  	FOREIGN KEY (place_start)
  	REFERENCES place(place_id),

  	FOREIGN KEY (place_finish)
  	REFERENCES place(place_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;
