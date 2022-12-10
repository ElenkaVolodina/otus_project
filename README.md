## Stream processing

### Домашняя работа № 9

Взаимодействие сервисов с использованием брокера сообщений RabbitMq


### Запуск приложения
```shell
kubectl create namespace otus-hw-9-volodina
helm upgrade --install -n otus-hw-9-volodina otus-hw-9-volodina ./hw_9_chart
# Установка rabbitmq
helm upgrade --install -n otus-hw-9-volodina otus-hw-rabbitmq --set auth.username=admin,auth.password=admin bitnami/rabbitmq
# Проброс порта
kubectl port-forward --namespace otus-hw-9-volodina svc/otus-hw-rabbitmq 15672:15672
```

### Удаление приложения
```shell
helm uninstall otus-hw-9-volodina -n otus-hw-9-volodina
```

### Postman коллекция
```shell
newman run tests/otus_hw_9.postman_collection.json --delay-request 2000
```

```shell
newman

otus_hw_9

→ Registration user_1
  POST arch.homework/registration [200 OK, 966B, 500ms]
  ✓  Registration user_1 status code is 200

→ Login user_1
  POST arch.homework/login [200 OK, 191B, 497ms]
  ✓  Login user_1 success

→ Check user in Pyment Service
  GET arch.homework/pyment/user/ [200 OK, 165B, 20ms]
  ┌
  │ 'Response body: ', { user_id: 259, id: 16, debit: 0 }
  └
  ✓  Check user in Pyment Service

→ Put money for user
  PUT arch.homework/pyment/put/ [200 OK, 135B, 34ms]
  ┌
  │ 'Response body: ', null
  └
  ✓  Create order 1 status code is 200

→ Check user in Pyment Service after put
  GET arch.homework/pyment/user/ [200 OK, 170B, 36ms]
  ┌
  │ 'Response body: ', { user_id: 259, id: 16, debit: 200000 }
  └
  ✓  Check user in Pyment Service

→ Create order 1
  POST arch.homework/create_order [200 OK, 250B, 50ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, hotel_id: 1, flight_id: 2, price: 100000, status: 'created'
  │ , id: 102, user_id: 259 }
  └
  ✓  Create order 1 status code is 200

→ Check order 1 in Order Service
  GET arch.homework/order/102/ [200 OK, 262B, 21ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, hotel_id: null, flight_id: null, price: 100000, status: 'pyment_ac
  │ cept', id: 102, user_id: 259 }
  └
  ✓  Check order 1 status

→ Check order 1 in Hotel Service
  GET arch.homework/hotel/order/102/ [200 OK, 201B, 90ms]
  ┌
  │ 'Response body: ', { hotel_id: 1, order_id: 102, status: 'accept', id: 66, user_id: 259 }
  └
  ✓  Check order 1 status

→ Check order 1 in Ticket Service
  GET arch.homework/ticket/order/102/ [200 OK, 202B, 36ms]
  ┌
  │ 'Response body: ', { flight_id: 2, order_id: 102, status: 'accept', id: 66, user_id: 259 }
  └
  ✓  Check order 1 status

→ Check order 1 in Notify Service
  GET arch.homework/notify/102/ [200 OK, 504B, 20ms]
  ┌
  │ 'Response body: ', [
  │   { order_id: 102, user_id: 259, subject: 'Создан новый заказ!', text: 'Добрый день! Создан заказ № 102. Мы уже работаем над ним.', id: 29 },
  │   { order_id: 102, user_id: 259, subject: 'Ваш заказ оплачен!', text: 'Добрый день! Ваш заказ № 102 успешно оплачен.', id: 30 }
  │ ]
  └
  ✓  Check order 1 status

→ Check user in Pyment Service after Order 1
  GET arch.homework/pyment/user/ [200 OK, 170B, 22ms]
  ┌
  │ 'Response body: ', { user_id: 259, id: 16, debit: 100000 }
  └
  ✓  Check user in Pyment Service after order 1

→ Create order 2
  POST arch.homework/create_order [200 OK, 255B, 32ms]
  ┌
  │ 'Response body: ', { address: 'address_new', count: 10, hotel_id: 2, flight_id: 4, price: 150000, status: 'created'
  │ , id: 103, user_id: 259 }
  └
  ✓  Create order 2 status code is 200

→ Check order 2 in Order Service
  GET arch.homework/order/103/ [200 OK, 262B, 19ms]
  ┌
  │ 'Response body: ', { address: 'address_new', count: 10, hotel_id: null, flight_id: null, price: 150000, status: 'canc
  │ eled', id: 103, user_id: 259 }
  └
  ✓  Check order 2 status

→ Check order 2 in Hotel Service
  GET arch.homework/hotel/order/103/ [200 OK, 203B, 27ms]
  ┌
  │ 'Response body: ', { hotel_id: 2, order_id: 103, status: 'canceled', id: 67, user_id: 259 }
  └
  ✓  Check order 2 status

→ Check order 2 in Ticket Service
  GET arch.homework/ticket/order/103/ [200 OK, 204B, 59ms]
  ┌
  │ 'Response body: ', { flight_id: 4, order_id: 103, status: 'canceled', id: 67, user_id: 259 }
  └
  ✓  Check order 2 status

→ Check order 2 in Notify Service
  GET arch.homework/notify/103/ [200 OK, 603B, 46ms]
  ┌
  │ 'Response body: ', [
  │   { order_id: 103, user_id: 259, subject: 'Создан новый заказ!', text: 'Добрый день! Создан заказ № 103. Мы уже работаем над ним.', id: 31 },
  │   { order_id: 103, user_id: 259, subject: 'Не удачная оплата заказа!', text: 'Добрый день! На Вашем счету недостаточно средств для оплаты заказа № 103. Заказ был отменен.'[39[39m
  │ m, id: 32 }
  │ ]
  └
  ✓  Check order 2 status

→ Check user in Pyment Service after Order 2
  GET arch.homework/pyment/user/ [200 OK, 170B, 19ms]
  ┌
  │ 'Response body: ', { user_id: 259, id: 16, debit: 100000 }
  └
  ✓  Check user in Pyment Service after order 2

→ Delete user_1
  DELETE arch.homework/user/delete [204 No Content, 120B, 27ms]

→ Logout user_1
  GET arch.homework/logout [200 OK, 147B, 15ms]
  ✓  Logout user1

┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                 19 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                 37 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                 19 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                 18 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 40.4s                                        │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 2.61kB (approx)                             │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 82ms [min: 15ms, max: 500ms, s.d.: 143ms] │
└──────────────────────────────────────────────────────────────────┘

```
