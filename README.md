# Env Vars

- DB_URL => database connection. Default: **postgresql://admin:admin@127.0.0.1:5432/thndr**
- MQTT_HOST => Default: **127.0.0.1**
- MQTT_PORT => Default: **1883**
- MQTT_TOPIC => Default: **thndr_trading**

# Endpoints

- *GET* **users/<int:user_id>**
- *GET* **stocks/<stock_id>**
- *PATCH/PUT* **/withdraw**
- *PATCH/PUT* **/deposit**
- *POST* **/sell**
- *POST* **/buy**

# Remarks:
- db gets populated with the following user ids **1,2,3,4**. User id is of type int