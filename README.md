# Checque-details-extraction-by-using-Tesseract

In this project, the details on the Cheque are extracted and returned in the JSON format. We use Tesseract OCR to convert the image to text. 
One must download tesseract to use this program. There are different types of cheques. In this project I have written two different codes persnal.py and cashier.py for different types of cheques.
The persnal code can be used for personal and payroll types of cheques. The cashier code is used for the cashier cheques. 
I have created a RESTApi for the project.

## Steps for the implementation

1. Install the neccessary packages and Tesseract OCR
2. First run the read_check.py file in the cmd it will run o the local host
3. The default input gven is to use the persnal type and the default image is check.png. To change, change the type in the BASE line of inp.py and change the image as well. Makesure the image you want is in the same folder as inp.py file.
4. After running the read_check.py run the inp.py in another cmd prompt. The results are obtained and printed. 
