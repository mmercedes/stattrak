FROM python:2.7

COPY app /

RUN pip install virtualenv
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /start.sh

CMD ["/start.sh"]
