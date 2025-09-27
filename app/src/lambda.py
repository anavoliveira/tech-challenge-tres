import requests
import pandas as pd
import boto3
import json
import os
from datetime import datetime

LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")
API_KEY = os.getenv("API_KEY")


def create_df(data):
  date = datetime.fromtimestamp(data["dt"])
  print(f"Data e hora da medição: {date}")

  data_df = {
    "weather_id": data["weather"][0]["id"],
    "weather_main" : data["weather"][0]["main"],
    "temp" : data["main"]["temp"],
    "temp_feels_like" : data["main"]["feels_like"],
    "temp_min" : data["main"]["temp_min"],
    "temp_max" : data["main"]["temp_max"],
    "pressure" : data["main"]["pressure"],
    "humidity" : data["main"]["humidity"],
    "wind_speed" : data["wind"]["speed"],
    "wind_deg" : data["wind"]["deg"],
    "clouds_all" : data["clouds"]["all"],
    "year" : date.year,
    "month" : date.month,
    "day" : date.day,
    "hour" : date.hour,
    "day_duration": data["sys"]["sunset"] - data["sys"]["sunrise"]
  }

  df = pd.DataFrame([data_df])
  print(df)
  return df


def create_s3_object(df):
  s3 = boto3.client('s3')

  year = df["year"].iloc[0]
  month = df["month"].iloc[0]
  day = df["day"].iloc[0]
  hour = df["hour"].iloc[0]
  print(f"Data e hora da medição: {year}-{month}-{day} {hour}:00:00")
  bucket_name = os.getenv("BUCKET_NAME")
  file_path = "/tmp/weather_data.parquet"
  object_name = f"weather_data/raw/{year}{month}{day}{hour}.parquet"

  df.to_parquet(f"/tmp/weather_data.parquet", index=False, engine='pyarrow')

  try:
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"Arquivo {object_name} enviado com sucesso para o bucket {bucket_name}.")
  except Exception as e:
    print(f"Erro ao enviar o arquivo: {e}")


def lambda_handler(event, context):

    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}"

    params = {
        "appid": API_KEY,
        "units": "metric",  # temperatura em °C
        "lang": "pt"        # descrição em português
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        print("Requisição bem-sucedida. Dados recebidos:")
        df = create_df(data)
        create_s3_object(df)

    except Exception as exception:
        print("Erro ao fazer a requisição:", exception)
        return {
        "statusCode": 500,
        "body": json.dumps({"error": "Erro ao fazer a requisição"})
        }

    return {
      "statusCode": 200,
      "body": json.dumps({"success": "Execucao realizada com sucesso"})
      }


if __name__ == "__main__":
  lambda_handler(None, None)