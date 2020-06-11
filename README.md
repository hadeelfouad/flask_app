# Env Vars

- DEBUG_MODE => true/false. Default: **false**
- DB_URL => database connection. Default: **postgresql://admin:admin@localhost:5432/thndr**
- MQTT_HOST => Default: **127.0.0.1**
- MQTT_PORT => Default: **1883**
- MQTT_TOPIC => Default: **thndr_trading**

# Endpoints

- *GET* **users/<user_id>**
- *GET* **stocks/<stock_id>**
- *PATCH/PUT* **/withdraw**
- *PATCH/PUT* **deposit**