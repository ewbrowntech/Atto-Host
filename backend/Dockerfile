FROM python:3.11
WORKDIR /app

# Install Poetry for dependency management
RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the rest of your application's code
COPY . /app

# Give execution rights to the entrypoint script
RUN chmod +x entrypoint.sh

# Apply the available migrations to the databse
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the FastAPI app
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0"]