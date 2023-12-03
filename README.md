
  <h1>Dazzle_Umbrella</h1>
  

  <p>Dazzle_Umbrella is a single-vendor e-commerce platform specialized in selling umbrellas. Built with Django and PostgreSQL, this project provides a robust framework for managing inventory, processing orders, and creating an engaging shopping experience for users.</p>

  <h2>Features</h2>
  <ul>
    <li><strong>User-Friendly Interface:</strong> Utilizing Bootstrap, the frontend offers an intuitive and responsive design, ensuring an enjoyable browsing and shopping experience across devices.</li>
    <li><strong>Product Management:</strong> Easily manage your umbrella inventory, including details like images, descriptions, and stock levels.</li>
    <li><strong>Order Processing:</strong> Streamlined order processing system for efficient handling of customer purchases.</li>
    <li><strong>Authentication & Authorization:</strong> Secure user authentication and authorization mechanisms to protect sensitive information and manage access levels.</li>
    <li><strong>Search & Filtering:</strong> Enable users to quickly find their desired umbrellas using search and filtering functionalities.</li>
  </ul>

  <h2>Technologies Used</h2>
  <ul>
    <li><strong>Django:</strong> Python-based web framework used for building the backend logic and handling requests.</li>
    <li><strong>PostgreSQL:</strong> Robust open-source relational database management system employed for data storage and retrieval.</li>
    <li><strong>Bootstrap:</strong> Frontend framework for designing and developing responsive and mobile-first websites.</li>
  </ul>

  <h2>Installation</h2>
  <ol>
    <li><strong>Clone the Repository:</strong>
      <pre><code>git clone https://github.com/4jd46k/Dazzle_ecom.git</code></pre>
    </li>
    <li>
  </ol>
  <ol>
    <p>
      # Navigate to the project directory
      <br>
      <pre><code>cd Dazzle_ecom</code></pre>
      <br>
      <strong>Setup Virtual Environment (Recommended):</strong>
      <br>
      # Create a virtual environment (optional but recommended)
      <br>
      <pre><code>python -m venv env</code></pre>
      <br>
      # Activate the virtual environment
      <br>
      # On Windows
      <br>
      <pre><code>.\env\Scripts\activate</code></pre>
      <br>
      # On macOS and Linux
      <br>
      <pre><code>source env/bin/activate</code></pre>
    </p>
    </li>
    <li>
    </li>
  </ol>
  <ol>
    <li>
    <strong>Install Dependencies:</strong>
      <p>
        <pre><code>pip install -r requirements.txt</code></pre>
      </p>
    </li>
  </ol>
  <ol>
    <li>
    <strong>Database Setup:</strong>
      <p>
        Configure PostgreSQL settings in settings.py.
        <br>
        Run migrations:
        <br>
        <pre><code>python manage.py makemigrations</code></pre>
        <br>
        <pre><code>python manage.py migrate</code></pre>
      </p>
    </li>
  </ol>
   <ol>
    <li>
    <strong>Run the Application:</strong>
      <p>
        <pre>python manage.py runserver</pre>
      </p>
     <p>
       Open a web browser and go to http://127.0.0.1:8000/ to view the application.
     </p>
    </li>
  </ol>
  <ol>
    
  



