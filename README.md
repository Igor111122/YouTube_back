# YouTube_back
Setting up the development environment:
1.Install Python: First of all, you need to have Python installed on your computer. You can download Python from the official website and install it.

2. Create a virtual environment: It is recommended to use a virtual environment to isolate the dependencies of your project. Open a command prompt and type:

-python -m venv venv
This will create a virtual environment named "venv".

3. Activate the virtual environment: Depending on your operating system, activate the virtual environment. For example, on Windows:
-venv\Scripts\activate

On macOS and Linux:
-source venv/bin/activate

4.Install dependencies: Go to the root folder of your project and install all necessary dependencies listed in requirements.txt using the command:

-pip install -r requirements.txt

Launching the application:
5.Start the Flask application: Open a command prompt and navigate to the root folder of your project. Enter the following command to launch the Flask application:

-python your_app.py
Use your app file name instead of your_app.py.

6.App Access: Your API must be accessible at http://localhost:5000.
