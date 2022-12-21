FROM python:3.8
ADD src/bot.py /server/src/
ADD src/keyboards.py /server/src/
ADD main.py /server/
ADD .env /server/
ADD src/variables.py /server/src/
ADD src/weather_worker.py /server/src/
WORKDIR /server/
RUN python3 -m pip install --user aiogram
RUN python3 -m pip install --user aioredis
RUN python3 -m pip install --user python-dotenv
#RUN python3 main.py
