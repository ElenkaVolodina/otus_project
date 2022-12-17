## Проектная работа

### Проектирование сервиса покупки туристических путевок с использованием микросервисной архитектуры


### Запуск приложения
```shell
kubectl create namespace otus-hw-volodina
# Установка rabbitmq
helm upgrade --install -n otus-hw-volodina otus-hw-rabbitmq --set auth.username=admin,auth.password=admin bitnami/rabbitmq

helm upgrade --install -n otus-hw-volodina otus-hw-volodina ./hw_chart
# Проброс порта
kubectl port-forward --namespace otus-hw-volodina svc/otus-hw-rabbitmq 15672:15672
```

### Установка  Prometheus
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace prometheus-operator
helm upgrade --install -n otus-hw-volodina stack prometheus-community/kube-prometheus-stack -f prometheus/prometheus-operator-values.yaml
```
### Включение метрик nginx
```shell
helm upgrade --install nginx ingress-nginx/ingress-nginx --namespace m -f nginx-ingress.yaml
```

### Удаление приложения
```shell
helm uninstall otus-hw-volodina -n otus-hw-volodina
```

### Postman коллекции
```shell
newman run tests/otus_hw.postman_collection.json --delay-request 2000
```

```shell
newman

otus_hw_9

→ Registration user_1
  POST poleteli.com/registration [200 OK, 966B, 433ms]
  ✓  Registration user_1 status code is 200

→ Login user_1
  POST poleteli.com/login [200 OK, 191B, 332ms]
  ✓  Login user_1 success

→ Check user in Pyment Service
  GET poleteli.com/payment/user/ [200 OK, 165B, 24ms]
  ┌
  │ 'Response body: ', { user_id: 268, id: 25, debit: 0 }
  └
  ✓  Check user in Pyment Service

→ Put money for user
  PUT poleteli.com/payment/put/ [200 OK, 135B, 15ms]
  ┌
  │ 'Response body: ', null
  └
  ✓  Create order 1 status code is 200

→ Check user in Pyment Service after put
  GET poleteli.com/payment/user/ [200 OK, 170B, 17ms]
  ┌
  │ 'Response body: ', { user_id: 268, id: 25, debit: 200000 }
  └
  ✓  Check user in Pyment Service

→ Create order 1
  POST poleteli.com/create_order [200 OK, 293B, 47ms]
  ┌
  │ 'Response body: ', { count: 1, hotel_id: 1, flight_id: 2, country_id: 1, price: 100000, date_from: '2023-01-31'[39[39m
  │ m, date_to: '2023-02-10', status: 'created', id: 112, user_id: 268 }
  └
  ✓  Create order 1 status code is 200

→ Check order 1 in Order Service
  GET poleteli.com/order/112/ [200 OK, 299B, 15ms]
  ┌
  │ 'Response body: ', { count: 1, hotel_id: 1, flight_id: 2, country_id: 1, price: 100000, date_from: '2023-01-31'[39[39m
  │ m, date_to: '2023-02-10', status: 'pyment_accept', id: 112, user_id: 268 }
  └
  ✓  Check order 1 status

→ Check order 1 in Hotel Service
  GET poleteli.com/hotel/order/112/ [200 OK, 201B, 23ms]
  ┌
  │ 'Response body: ', { hotel_id: 1, order_id: 112, status: 'accept', id: 76, user_id: 268 }
  └
  ✓  Check order 1 status

→ Check order 1 in Ticket Service
  GET poleteli.com/ticket/order/112/ [200 OK, 202B, 35ms]
  ┌
  │ 'Response body: ', { flight_id: 2, order_id: 112, status: 'accept', id: 76, user_id: 268 }
  └
  ✓  Check order 1 status

→ Check order 1 in Notify Service
  GET poleteli.com/notify/112/ [200 OK, 504B, 27ms]
  ┌
  │ 'Response body: ', [
  │   { order_id: 112, user_id: 268, subject: 'Создан новый заказ!', text: 'Добрый день! Создан заказ № 112. Мы уже работаем над ним.', id: 49 },
  │   { order_id: 112, user_id: 268, subject: 'Ваш заказ оплачен!', text: 'Добрый день! Ваш заказ № 112 успешно оплачен.', id: 50 }
  │ ]
  └
  ✓  Check order 1 status

→ Check user in Pyment Service after Order 1
  GET poleteli.com/payment/user/ [200 OK, 170B, 12ms]
  ┌
  │ 'Response body: ', { user_id: 268, id: 25, debit: 100000 }
  └
  ✓  Check user in Pyment Service after order 1

→ Create order 2
  POST poleteli.com/create_order [200 OK, 295B, 23ms]
  ┌
  │ 'Response body: ', { count: 2, hotel_id: 21, flight_id: 12, country_id: 1, price: 250000, date_from: '2023-07-31'[[39m
  │ 39m, date_to: '2023-08-10', status: 'created', id: 113, user_id: 268 }
  └
  ✓  Create order 2 status code is 200

→ Check order 2 in Order Service
  GET poleteli.com/order/113/ [200 OK, 296B, 14ms]
  ┌
  │ 'Response body: ', { count: 2, hotel_id: 21, flight_id: 12, country_id: 1, price: 250000, date_from: '2023-07-31'[[39m
  │ 39m, date_to: '2023-08-10', status: 'canceled', id: 113, user_id: 268 }
  └
  ✓  Check order 2 status

→ Check order 2 in Hotel Service
  GET poleteli.com/hotel/order/113/ [200 OK, 204B, 39ms]
  ┌
  │ 'Response body: ', { hotel_id: 21, order_id: 113, status: 'canceled', id: 77, user_id: 268 }
  └
  ✓  Check order 2 status

→ Check order 2 in Ticket Service
  GET poleteli.com/ticket/order/113/ [200 OK, 205B, 20ms]
  ┌
  │ 'Response body: ', { flight_id: 12, order_id: 113, status: 'canceled', id: 77, user_id: 268 }
  └
  ✓  Check order 2 status

→ Check order 2 in Notify Service
  GET poleteli.com/notify/113/ [200 OK, 603B, 18ms]
  ┌
  │ 'Response body: ', [
  │   { order_id: 113, user_id: 268, subject: 'Создан новый заказ!', text: 'Добрый день! Создан заказ № 113. Мы уже работаем над ним.', id: 51 },
  │   { order_id: 113, user_id: 268, subject: 'Не удачная оплата заказа!', text: 'Добрый день! На Вашем счету недостаточно средств для оплаты заказа № 113. Заказ был отменен.'[39[39m
  │ m, id: 52 }
  │ ]
  └
  ✓  Check order 2 status

→ Check user in Pyment Service after Order 2
  GET poleteli.com/payment/user/ [200 OK, 170B, 13ms]
  ┌
  │ 'Response body: ', { user_id: 268, id: 25, debit: 100000 }
  └
  ✓  Check user in Pyment Service after order 2

→ Delete user_1
  DELETE poleteli.com/user/delete [204 No Content, 120B, 32ms]

→ Logout user_1
  GET poleteli.com/logout [200 OK, 147B, 5ms]
  ✓  Logout user1

┌─────────────────────────┬───────────────────┬───────────────────┐
│                         │          executed │            failed │
├─────────────────────────┼───────────────────┼───────────────────┤
│              iterations │                 1 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│                requests │                19 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│            test-scripts │                37 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│      prerequest-scripts │                19 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│              assertions │                18 │                 0 │
├─────────────────────────┴───────────────────┴───────────────────┤
│ total run duration: 11.2s                                       │
├─────────────────────────────────────────────────────────────────┤
│ total data received: 2.77kB (approx)                            │
├─────────────────────────────────────────────────────────────────┤
│ average response time: 60ms [min: 5ms, max: 433ms, s.d.: 112ms] │
└─────────────────────────────────────────────────────────────────┘


```

```shell
newman run tests/otus_hw_catalog.postman_collection.json
```

```shell
newman

otus_hw_catalog

→ Registration user
  POST poleteli.com/registration [200 OK, 966B, 337ms]
  ✓  Registration user_1 status code is 200

→ Login user
  POST poleteli.com/login [200 OK, 191B, 334ms]
  ✓  Login user_1 success

→ Create catalog
  POST poleteli.com/catalog/create_voucher [200 OK, 251B, 19ms]
  ┌
  │ 'Response body: ', { flight_id: 12, hotel_id: 321, country_id: 1, date_from: '2023-07-31', date_to: '2023-08-10', price:
  │  250000, id: 3 }
  └
  ✓  Create new item status code is 200

→ Find
  POST poleteli.com/catalog/search [200 OK, 253B, 12ms]
  ┌
  │ 'Response body: ', [ { flight_id: 12, hotel_id: 321, country_id: 1, date_from: '2023-07-31', date_to: '2023-08-10', price[39[39m
  │ m: 250000, id: 3 } ]
  └
  ✓  Find voucher

→ Create catalog from queue
  GET poleteli.com/catalog/send-message [200 OK, 147B, 9ms]
  ┌
  │ 'Response body: ', { status: 'ok' }
  └
  ✓  Create new item from queue status code is 200

→ Find
  POST poleteli.com/catalog/search [200 OK, 374B, 14ms]
  ┌
  │ 'Response body: ', [
  │   { flight_id: 12, hotel_id: 321, country_id: 1, date_from: '2023-07-31', date_to: '2023-08-10', price: 250000, id: [33[39m
  │ m3 },
  │   { flight_id: 123, hotel_id: 321, country_id: 3, date_from: '2023-01-31', date_to: '2023-02-10', price: 1234567, id: [[39m
  │ 33m4 }
  │ ]
  └
  ✓  Find voucher

→ Delete user
  DELETE poleteli.com/user/delete [204 No Content, 120B, 13ms]

→ Logout user
  GET poleteli.com/logout [200 OK, 147B, 7ms]
  ✓  Logout user1

┌─────────────────────────┬───────────────────┬───────────────────┐
│                         │          executed │            failed │
├─────────────────────────┼───────────────────┼───────────────────┤
│              iterations │                 1 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│                requests │                 8 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│            test-scripts │                15 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│      prerequest-scripts │                 8 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│              assertions │                 7 │                 0 │
├─────────────────────────┴───────────────────┴───────────────────┤
│ total run duration: 972ms                                       │
├─────────────────────────────────────────────────────────────────┤
│ total data received: 1.33kB (approx)                            │
├─────────────────────────────────────────────────────────────────┤
│ average response time: 93ms [min: 7ms, max: 337ms, s.d.: 139ms] │
└─────────────────────────────────────────────────────────────────┘

```
