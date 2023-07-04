FROM mcr.microsoft.com/devcontainers/anaconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# Install additional OS packages using apt-get
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git

# Set the working directory inside the container
WORKDIR /app

# Copy your Spotify API code into the container
COPY . /app

# Install any additional dependencies for your Spotify API
RUN pip install -r requirements.txt

# Expose the port your Spotify API will be running on
EXPOSE 5000

# Set the command to run your Spotify API when the container starts
CMD [ "python", "app.py" ]
