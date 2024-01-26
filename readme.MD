create  an image
docker build -t flask-e-commerce .

run the container
docker run -d -p 5002:5000 -w /app -v "$(pwd):/app" flask-e-commerce

-w - Current working directory of the container

-v - Linking the pwd(host) to work directory of the container
