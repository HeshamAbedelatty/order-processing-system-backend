# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /OrderProcessingSystem

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Install djangorestframework_simplejwt
Run pip install djangorestframework_simplejwt

# Copy the rest of your Django project code into the container
COPY . .

# Expose the port on which the Django application will run
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]