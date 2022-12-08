## Распределенные транзакции

### Домашняя работа № 8

Механизм распределенной транзакции реализован на основе Саги, со способом координации - хореография.
Шина - RabbitMq


### Запуск приложения
```shell
kubectl create namespace otus-hw-8-volodina
helm upgrade --install -n otus-hw-8-volodina otus-hw-8-volodina ./hw_8_chart
# Установка rabbitmq
helm upgrade --install -n otus-hw-8-volodina otus-hw-rabbitmq --set auth.username=admin,auth.password=admin bitnami/rabbitmq
# Проброс порта для настройки
kubectl port-forward --namespace otus-hw-8-volodina svc/otus-hw-rabbitmq 15672:15672
```

После запуска необходимо сделать настройки rabbitmq. 
А именно, создать exchange и binding

### Удаление приложения
```shell
helm uninstall otus-hw-8-volodina -n otus-hw-8-volodina
```

### Postman коллекция
```shell
newman run tests/otus_hw_8.postman_collection.json
```

```shell
newman

otus_hw_8

→ Registration user_1
  POST arch.homework/registration [200 OK, 966B, 1469ms]
  ✓  Registration user_1 status code is 200

→ Login user_1
  POST arch.homework/login [200 OK, 191B, 4.9s]
  ✓  Login user_1 success

→ Create order 1
  POST arch.homework/create_order [200 OK, 231B, 115ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, hotel_id: 1, flight_id: 2, status: 'created', id: 52, 
  │ user_id: 213 }
  └
  ✓  Create order 1 status code is 200

→ Check order 1 in Order Service
  GET arch.homework/order/52/ [200 OK, 238B, 220ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, hotel_id: null, flight_id: null, status: 'created', id: 52, [39m
  │ [37muser_id: 213 }
  └
  ✓  Check order 1 status

→ Check order 1 in Hotel Service Copy
  GET arch.homework/hotel/order/52/ [200 OK, 201B, 201ms]
  ┌
  │ 'Response body: ', { hotel_id: 1, order_id: 52, status: 'pending', id: 20, user_id: 213 }
  └
  ✓  Check order 1 status

→ Check order 1 in Ticket Service Copy
  GET arch.homework/ticket/order/52/ [200 OK, 202B, 185ms]
  ┌
  │ 'Response body: ', { flight_id: 2, order_id: 52, status: 'pending', id: 20, user_id: 213 }
  └
  ✓  Check order 1 status

→ Create order 2
  POST arch.homework/create_order [200 OK, 238B, 137ms]
  ┌
  │ 'Response body: ', { address: 'address_new', count: 10, hotel_id: 11, flight_id: 4, status: 'created', id: 53,
  │  user_id: 213 }
  └
  ✓  Create order 2 status code is 200

→ Check order 2 in Order Service
  GET arch.homework/order/53/ [200 OK, 244B, 362ms]
  ┌
  │ 'Response body: ', { address: 'address_new', count: 10, hotel_id: null, flight_id: null, status: 'canceled', id: 53[[39m
  │ 39m, user_id: 213 }
  └
  ✓  Check order 2 status

→ Check order 2 in Hotel Service
  GET arch.homework/hotel/order/53/ [200 OK, 203B, 57ms]
  ┌
  │ 'Response body: ', { hotel_id: 11, order_id: 53, status: 'canceled', id: 21, user_id: 213 }
  └
  ✓  Check order 2 status

→ Check order 2 in Ticket Service
  GET arch.homework/ticket/order/53/ [200 OK, 203B, 128ms]
  ┌
  │ 'Response body: ', { flight_id: 4, order_id: 53, status: 'canceled', id: 21, user_id: 213 }
  └
  ✓  Check order 1 status

→ Delete user_1
  DELETE arch.homework/user/delete [204 No Content, 120B, 139ms]

→ Logout user_1
  GET arch.homework/logout [200 OK, 147B, 31ms]
  ✓  Logout user1

┌─────────────────────────┬────────────────────┬────────────────────┐
│                         │           executed │             failed │
├─────────────────────────┼────────────────────┼────────────────────┤
│              iterations │                  1 │                  0 │
├─────────────────────────┼────────────────────┼────────────────────┤
│                requests │                 12 │                  0 │
├─────────────────────────┼────────────────────┼────────────────────┤
│            test-scripts │                 23 │                  0 │
├─────────────────────────┼────────────────────┼────────────────────┤
│      prerequest-scripts │                 12 │                  0 │
├─────────────────────────┼────────────────────┼────────────────────┤
│              assertions │                 11 │                  0 │
├─────────────────────────┴────────────────────┴────────────────────┤
│ total run duration: 8.7s                                          │
├───────────────────────────────────────────────────────────────────┤
│ total data received: 1.54kB (approx)                              │
├───────────────────────────────────────────────────────────────────┤
│ average response time: 662ms [min: 31ms, max: 4.9s, s.d.: 1331ms] │
└───────────────────────────────────────────────────────────────────┘


```
