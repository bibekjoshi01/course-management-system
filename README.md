## Course Management System

This is a simple course management system built with Django. It includes features for course creation, student enrollment, and an admin dashboard to manage courses and students.

### Features
- **Admin Features**:
  - Create categories (supports parent-child relationships).
  - Create courses with videos, documents, and MCQ quizzes.
  - Enroll students in courses.
  - View a list of enrolled students per course.
- **Student Features**:
  - Receive an email with login credentials upon registration.
  - Enrolled students can access their assigned courses.
- **Content Management**:
  - Upload videos (Max: 50MB, `.mp4` only).
  - Upload documents (Max: 10MB, `.pdf` only).
  - Create MCQ quizzes with multiple correct answers.
- **UI**:
  - Custom Bootstrap-based dashboard for admin.
  - Django templates for rendering course lists.

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/django-course-management.git
   cd django-course-management
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements/local.txt # On Windows: pip install -r requirements\local.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Admin Panel**:
   - Open `http://127.0.0.1:8000/admin/`
   - Log in using the superuser credentials.

### Configuration
- Update `.env` with your Google SMTP credentials for email functionality.
