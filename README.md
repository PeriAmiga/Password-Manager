<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>Password Manager Application</h1>

  <p>This is a password manager application developed in Python. It allows users to securely store, manage, and organize their passwords.</p>

  <img src="Password-Manager - Manager.png" alt="Password Manager Screenshot" style="display:block; margin:auto; max-width:100%;">

  <h2>Instructions</h2>

  <h3>Initial Setup</h3>

  <ol>
    <li><strong>Update Configuration:</strong> In the first run, you need to update the data in the <code>configuration.py</code> file according to your database configuration.</li>
    <li><strong>Database Setup:</strong> Run the <code>dbCodeCreation.py</code> file to initialize the required database tables and configurations.</li>
    <li><strong>Cryptography Setup:</strong> Run the <code>my_cryptography.py</code> file to set up encryption and decryption functionalities.</li>
  </ol>

  <h3>Running the Application</h3>

  <p>After completing the initial setup steps:</p>

  <ol>
    <li>Run the <code>main.py</code> file to start the password manager application.</li>
  </ol>

  <h2>Features</h2>

  <ul>
    <li>Securely store, manage, and organize passwords.</li>
    <li>Import passwords from CSV files, including CSV files exported from Google Password Manager.</li>
    <li>Export passwords to CSV files compatible with Google Password Manager.</li>
    <li>Generate random passwords.</li>
    <li>Reset password via email.</li>
    <li>Change password for added security.</li>
    <li>Secure login and registration functionality.</li>
    <li>Search passwords by application name or URL.</li>
  </ul>

  <h2>Dependencies</h2>

  <ul>
    <li>Python 3.x</li>
    <li>MySQL database</li>
  </ul>

  <h2>Technologies and Libraries Used</h2>

  <ul>
    <li><strong>Python:</strong> Used as the primary programming language for development.</li>
    <li><strong>Tkinter:</strong> Used for building the graphical user interface (GUI).</li>
    <li><strong>Pandas:</strong> Used for data manipulation and CSV file handling.</li>
    <li><strong>MySQL Connector:</strong> Used to connect and interact with the MySQL database.</li>
    <li><strong>SMTPLib:</strong> Used for sending emails for password reset functionality.</li>
    <li><strong>Hashlib:</strong> Used for hashing passwords.</li>
    <li><strong>PBKDF2:</strong> Used for key derivation.</li>
    <li><strong>Cryptography:</strong> Used for symmetric encryption and decryption.</li>
  </ul>

  <h2>Usage</h2>

  <ol>
    <li>Clone the repository:</li>
  </ol>

  <pre><code>git clone https://github.com/PeriAmiga/password-manager.git</code></pre>

  <ol start="2">
    <li>Navigate to the project directory:</li>
  </ol>

  <pre><code>cd password-manager</code></pre>

  <ol start="3">
    <li>Follow the initial setup instructions mentioned above.</li>
    <li>Run the application:</li>
  </ol>

  <pre><code>python main.py</code></pre>


</body>
</html>