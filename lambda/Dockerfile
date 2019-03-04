FROM lambci/lambda:build-python3.6

COPY ./requirements /requirements

RUN python -m venv /ve && \
    source /ve/bin/activate && \
    pip install -r /requirements/lambda.txt

ENV FLASK_APP marvin.py
ENV FLASK_CONFIG production

RUN echo 'export PS1="\[\e[36m\]λ.shell>\[\e[m\] "' >> /root/.bashrc

COPY ./lambda/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
