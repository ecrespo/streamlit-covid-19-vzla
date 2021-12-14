FROM python:3.10.0b4

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

CMD cd ./covid19 && git pull ; cd ..

WORKDIR /app
ADD . /app

# Install dependencies
RUN pip install -r requirements.txt

# copying all files over
COPY . /app

# Expose port 
ENV PORT 8501


# cmd to launch app when container is run
CMD streamlit run app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
mkdir -p ~/.streamlit/
RUN bash -c 'echo -e "\
    [general]\n\
    \"ecrespo@gmail.com\"\n\
    " > ~/.streamlit/credentials.toml

RUN bash -c 'echo -e "\
    [server]\n\
    enableCORS = false\n\
    " > ~/.streamlit/config.toml'
