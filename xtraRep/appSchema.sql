CREATE TABLE appUsers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL,
    dateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appUserCredentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appUserID INT NOT NULL,
    /*still being built */
);