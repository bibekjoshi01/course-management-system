## Course Management System

This is a simple course management system built with Django. It includes features for course creation, student enrollment, and an admin dashboard to manage courses and students.

### Follow the below step to run the project

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bibekjoshi01/course-management-system.git
   cd django-course-management
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:

- Make sure you have `.env` with proper required variables listed in
- Update `.env` with your Google SMTP credentials for email functionality.

5. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the Django Admin Panel**:

   - Open Django Admin: `http://127.0.0.1:8000/admin/`
   - Log in using the superuser credentials.

9. **Access the Dashboard**
   - Open Dashboard: `https://127.0.0.1:8000`
