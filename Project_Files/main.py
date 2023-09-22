from socket import *
from utils import *
import os
#Setting Up Path Variables
PATH_EN_html = "HTML_Files\\main_en.html"
PATH_AR_html = "HTML_Files\\main_ar.html"
PATH_Not_Found_html = "HTML_Files\\Oops.html"
PATH_Home_html = "HTML_Files\\home_page.html"


#Creating the Socket
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")




flag = 0

#Loop to Process Different Requests
while True:
    try:
        #Recieving the Requests and obtaining the IP and Port
        connectionSocket, addr = serverSocket.accept()
        ip = addr[0]
        port = addr[1]
        print('Got connection from', "IP: " + ip + ", Port: " + str(port))
        sentence = connectionSocket.recv(1024).decode()

        #Splitting the Request to use in IF statements
        request_lines = sentence.split('\r\n')
        print(sentence)
        if len(request_lines) > 0:
            first_line = request_lines[0]
            parts = first_line.split(' ')
            if len(parts) > 1:
                requested_url = parts[1]

        split_url = os.path.split(requested_url)[-1]



        #if-Statements to open different pages
        if requested_url == "/ar" or requested_url == "/main_ar.html":
            pathToOpen = PATH_AR_html

        elif requested_url == "/en" or requested_url == "/main_en.html":
            pathToOpen = PATH_EN_html

        elif requested_url == "/" or requested_url == "/index.html":
            pathToOpen = PATH_Home_html

        #Redirecting to Specified Websites
        elif requested_url == "/azn":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send("Location: https://www.amazon.com\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            continue

        elif requested_url == "/so":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send("Location: https://stackoverflow.com\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            continue

        elif requested_url == "/bzu":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send("Location: https://www.birzeit.edu\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            continue







        elif requested_url == "/SortByPrice" or requested_url == "/SortByName":
            #Initializing an array to store laptop data from the text file
            array = read_file("HTML_Files\\Text_Files\\laptops.txt")

            if requested_url == "/SortByPrice":
                sort_by_price(array)
            else:
                sort_by_name(array)

            # Sample arrays of laptop names and prices
            laptop_names = array[0]
            laptop_prices = array[1]

            # Initialize the HTML content with the table structure and embedded CSS
            table_content = """
      
            
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>ENCS3320 project 1210708</title>
    <style>
        /* Style for the entire table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        /* Style for table header cells */
        th {
            
            padding: 10px;
            text-align: center;
            color: white; /* Text color */
        font-size: 38px; /* Font size */
        font-family: Arial, sans-serif; /* Font family */
        background-color: #020230;
        }



        /* Style for table data cells */
        td {
            padding: 10px;
            border: 1px solid #020230;
            background-color: #03a7d3;
            text-align: center;
             color: #020230; /* Text color */
        font-size: 24px; /* Font size */
        font-family: Arial, sans-serif; /* Font family */
        }

        /* Style for images */
        img {
            width: 200px;
            max-width: 400px;
            height: auto;
            max-height: 130px;
           border: 3px solid black;
        }
    </style>
</head>

<body>
    <table style="table-layout: fixed; width: 100%;">
        <colgroup>
            <col style="width: 25%;">
            <col style="width: 50%;">
            <col style="width: 25%;">
        </colgroup>
        <tr>
            <th>Image</th>
            <th>Name</th>
            <th>Price</th>
        </tr>
            """

            # Loop through each laptop name and price and add them to the table content
            for name, price in zip(laptop_names, laptop_prices):
                # Construct image path using the laptop name

                image_path = f"images\\{name.replace(' ', '_')}.jpg"

                table_content += f"<tr><td><img src='{image_path}' alt='{name}'></td><td>{name.upper()}</td><td>{price}</td></tr>"

            # Close the table structure and the HTML
            table_content += """
                </table>
            </body>
            </html>
            """
            # Defining the output directory and filename
            output_directory = "HTML_Files"
            output_filename = "laptops_sorted.html"
            output_path = f"{output_directory}/{output_filename}"

            # Create the output directory if it doesn't exist
            os.makedirs(output_directory, exist_ok=True)

            # Write the table content to the HTML file in the specified directory
            with open(output_path, "w") as html_file:
                html_file.write(table_content)
            pathToOpen = output_path

        #Checking for the case where the path is incorrect
        else:
            pathToOpen = PATH_Not_Found_html


        #if Statements to deal with different file types
        if split_url.endswith("png"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: image/png; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("HTML_Files/images/" + split_url, "rb")

        elif split_url.endswith("jpg"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: image/jpg; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("HTML_Files/images/" + split_url, "rb")

        elif split_url.endswith("css"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: text/css; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("HTML_Files/CSS_Files/" + split_url, "rb")

        elif split_url.endswith("html"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: text/css; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("HTML_Files/" + split_url, "rb")

        elif split_url.endswith("/") or requested_url == "/":
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open(pathToOpen, "rb")

        else:
            connectionSocket.send("HTTP/1.1 404 Not Found \r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open(pathToOpen, "rb")
            flag = 1

        data = f1.read()
        #Flag used to determine if the webpage doesn't exist
        if flag == 1:
            #Used to display the server port and IP in HTML error page
            data = data.replace(b"{IP_ADDRESS}", ip.encode()).replace(b"{PORT}", str(port).encode())
        connectionSocket.send(data)

        connectionSocket.close()

    except OSError:
        print("IO error")
else:
    print("OK")

