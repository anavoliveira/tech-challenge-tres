# WeatherSense — previsão e detecção de anomalias meteorológicas em tempo real


A  API do **OpenWeather** disponibiliza dados públicos, atualizações em tempo real, histórico sobre o clima, permitindo a criação de aplicações para prever chuva, temperatura, detectar anomalias, alimentar dashboards, acionar notificações etc.


**Objetivo:**
 - Coletar dados do OpenWeather em tempo real.
 - Armazenar em um bucket S3.
 - Treinar um modelo que crie previsões da temperatura para diferentes horários durante o dia (11h, 16h e 21h).
 - Criar uma aplicação que realize a predição e envie as informações via email para os usuários todos os dias às 6h.

## Arquitetura

* **Ingestão:** Lambda + EventBridge que chama OpenWeather API a cada 60 min. 
* **Armazenamento:** S3 (raw / history / consolidate ).
* **Treino:** SageMaker Studio.
* **Serving (produção):** SageMaker endpoint (real-time).
* **Dashboard:** Streamlit hospedado em ECS.
* **Observability:** CloudWatch + logs + métricas de validade do dado.


## Dados Disponiveis

A subscrinção grátis da API disponibiliza os seguintes dados:

**Current Weather Data (Dados de Clima Atual)**
- Dados do clima atual para qualquer localização.
- Os dados são coletados e processados a partir de diferentes fontes, como modelos climáticos globais e locais, satélites, radares e uma vasta rede de estações meteorológicas.
- Formatos disponíveis: **JSON, XML e HTML**.

- **5 Day / 3 Hour Forecast (Previsão de 5 dias / intervalos de 3 horas)** 
- Previsão de 5 dias para qualquer localização no globo.
- Previsão detalhada em intervalos de 3 horas.
- Formatos disponíveis: **JSON e XML**.

**Weather Maps 1.0 (Mapas Meteorológicos)** 
- Inclui mapas de precipitação, nuvens, pressão, temperatura, vento e mais.
- Compatíveis como camadas em **Direct Tiles, OpenLayers, Leaflet e Google Maps**.

**Air Pollution API (API de Poluição do Ar)** 
- Dados atuais, previsão e históricos de poluição do ar.
- Previsão para até 4 dias à frente em intervalos de 1 hora.
- Inclui o **Índice de Qualidade do Ar (AQI)** e índices para **CO, NO, NO₂, O₃, SO₂, NH₃, PM2.5 e PM10**.

**Geocoding API (API de Geocodificação)** 
- Suporta métodos **direto e reverso**, funcionando com nomes de cidades, áreas e distritos, países e estados.
- Possibilita limitar quantas localizações com o mesmo nome ou coordenadas próximas aparecerão na resposta da API.

**Weather Stations (Estações Meteorológicas)** 
- API para gerenciamento de suas estações meteorológicas pessoais.
- Permite conectar as estações e transferir as medições.
- Receba as medições agregadas da esta


## Como utilizar a API

https://openweathermap.org/api/one-call-3#current



