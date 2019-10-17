import schedule
import time
import src.keras_model as keras_model


schedule.every().day.at("00:00").do(keras_model.train_model, 'It is 11:45')

while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
