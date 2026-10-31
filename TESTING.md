TESTING REPORT
Project Name
AutoCare Vehicle Management System

Testing Summary
Test Case ID	Module	Test Description	Expected Result	Status
TC001	Add Vehicle	Add a new vehicle with valid data	Vehicle added successfully	PASS
TC002	Add Vehicle	Add vehicle with empty fields	Validation error shown	PASS
TC003	Search Vehicle	Search existing vehicle	Vehicle details displayed	PASS
TC004	Search Vehicle	Search non-existing vehicle	Vehicle not found message shown	PASS
TC005	Delete Vehicle	Delete selected vehicle	Vehicle removed successfully	PASS
TC006	Database	Save vehicle data	Data stored in SQLite database	PASS
TC007	Service Due Checker	Check due vehicle service	Due status displayed correctly	PASS
TC008	GUI	Open application window	Application loads successfully	PASS
Testing Environment
Operating System: Windows 11
Programming Language: Python
GUI Framework: Tkinter
Database: SQLite
Test Result
Total Test Cases: 8

Passed: 8

Failed: 0

Success Rate: 100%

Conclusion
The AutoCare Vehicle Management System was tested successfully. All major functionalities including vehicle registration, search, deletion, database integration, and service due tracking worked as expected.