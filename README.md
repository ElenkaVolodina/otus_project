## Основы работы с Kubernetes

### Домашняя работа № 6

Для реализации идемпотентности использовался ключ идемпотентности,
который передается с клиента и хранится на сервере.


### Используемый Docker образ
```shell
docker pull elenkavolodina/otus_hw6
```

### Запуск приложения
```shell
kubectl create namespace otus-hw-6-volodina
helm upgrade --install -n otus-hw-6-volodina otus-hw-6-volodina ./hw_6_chart
```

### Удаление приложения
```shell
helm uninstall otus-hw-6-volodina -n otus-hw-6-volodina
```

### Postman коллекция
```shell
newman run tests/otus_hw_6.postman_collection.json
```

```shell
newman

otus_hw_6

→ Create order not authorization user
  POST arch.homework/create_order [401 Unauthorized, 308B, 58ms]
  ✓  Create order not authorization user

→ Registration user_1
  POST arch.homework/registration [200 OK, 966B, 364ms]
  ✓  Registration user_1 status code is 200

→ Login user_1
  POST arch.homework/login [200 OK, 191B, 350ms]
  ✓  Login user_1 success

→ Create order 1
  POST arch.homework/create_order [200 OK, 204B, 19ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, status: 'created', id: 11, user_id: 189 }
  └
  ✓  Create order 1 status code is 200

→ Create order 1 again
  POST arch.homework/create_order [200 OK, 204B, 18ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, status: 'created', id: 11, user_id: 189 }
  └
  ✓  Create order 1 agin return old order

→ Create order 1 and again
  POST arch.homework/create_order [200 OK, 204B, 18ms]
  ┌
  │ 'Response body: ', { address: 'address', count: 1, status: 'created', id: 11, user_id: 189 }
  └
  ✓  Create order 1 and agin return old order

→ Create order 2
  POST arch.homework/create_order [200 OK, 209B, 17ms]
  ┌
  │ 'Response body: ', { address: 'address_new', count: 10, status: 'created', id: 12, user_id: 189 }
  └
  ✓  Create order 2 status code is 200

→ Delete user_1
  DELETE arch.homework/user/delete [204 No Content, 120B, 14ms]

→ Logout user_1
  GET arch.homework/logout [200 OK, 147B, 7ms]
  ✓  Logout user1

┌─────────────────────────┬───────────────────┬───────────────────┐
│                         │          executed │            failed │
├─────────────────────────┼───────────────────┼───────────────────┤
│              iterations │                 1 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│                requests │                 9 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│            test-scripts │                17 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│      prerequest-scripts │                 9 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│              assertions │                 8 │                 0 │
├─────────────────────────┴───────────────────┴───────────────────┤
│ total run duration: 1144ms                                      │
├─────────────────────────────────────────────────────────────────┤
│ total data received: 1.31kB (approx)                            │
├─────────────────────────────────────────────────────────────────┤
│ average response time: 96ms [min: 7ms, max: 364ms, s.d.: 140ms] │
└─────────────────────────────────────────────────────────────────┘

```
