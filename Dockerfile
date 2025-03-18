# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install required dependencies
# Install required dependencies
# Install required dependencies
RUN pip install --no-cache-dir fastapi uvicorn xgboost numpy pandas joblib scikit-learn nltk==3.8.1 && \
    mkdir -p /root/nltk_data && \
    python -c "import nltk; nltk.data.path.append('/root/nltk_data'); \
               nltk.download('punkt', download_dir='/root/nltk_data'); \
               nltk.download('stopwords', download_dir='/root/nltk_data'); \
               nltk.download('omw-1.4', download_dir='/root/nltk_data'); \
               nltk.download('wordnet', download_dir='/root/nltk_data'); \
               nltk.download('averaged_perceptron_tagger', download_dir='/root/nltk_data'); \
               nltk.download('maxent_ne_chunker', download_dir='/root/nltk_data'); \
               nltk.download('words', download_dir='/root/nltk_data'); \
               nltk.download('tagsets', download_dir='/root/nltk_data'); \
               nltk.download('universal_tagset', download_dir='/root/nltk_data')"

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

