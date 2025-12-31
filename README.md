# Library-Management
Library Management System (Beginner Friendly)
This is a Python-based Library Management System developed as a beginner-level project using Tkinter GUI, MySQL database, and Barcode generation.
The main goal of this project is to understand how a desktop application works with:
•	Multiple pages (screens)
•	Database connectivity
•	Basic CRUD operations
•	Barcode generation
________________________________________
 Features
•	 Home Page
o	Admin Login
o	Student Page
o	Exit option
•	 Admin Page
o	Generate barcode for books/students
o	View all student records
•	 Student Page
o	Add student details
o	Assign book with barcode
•	 Barcode Generation
o	Uses python-barcode library
o	Saves barcode as an image
•	 Database Integration
o	MySQL database used to store records
o	Supports Insert and View operations
________________________________________
 Technologies Used
•	Programming Language: Python
•	GUI: Tkinter
•	Database: MySQL
•	Barcode: python-barcode
•	Image Handling: Pillow (PIL)
________________________________________
Database Table Structure
Table Name: student_data
Column Name	Description
S_ID	Student ID
F_Name	Student Name
Book_title	Book Name
Barcode	Book Barcode
________________________________________
 How to Run the Project
1.	Install required libraries:
2.	pip install mysql-connector-python python-barcode pillow
3.	Create MySQL database:
4.	CREATE DATABASE library;
5.	USE library;
6.	CREATE TABLE student_data (
	    S_ID INT,
	    F_Name VARCHAR(50),
	    Book_title VARCHAR(100),
	    Barcode VARCHAR(50));
11.	Update database credentials in the code:
12.	host="localhost"
13.	user="root"
14.	password="your_password"
15.	database="library"
16.	Run the Python file:
17.	python library_management.py
________________________________________
What I Learned from This Project
•	Creating GUI applications using Tkinter
•	Working with multiple pages using Frames
•	Connecting Python with MySQL
•	Performing basic database operations (Insert, Select)
•	Generating and displaying barcodes


