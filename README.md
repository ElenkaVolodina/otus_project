## Распределенные транзакции

### Домашняя работа № 8

Механизм распределенной транзакции реализован на основе Саги, со способом координации - хореография.
Шина - RabbitMq


### Запуск приложения
```shell
kubectl create namespace otus-hw-6-volodina
helm upgrade --install -n otus-hw-6-volodina otus-hw-6-volodina ./hw_6_chart
# Установка rabbitmq
helm upgrade --install -n otus-hw-2-volodina otus-hw-rabbitmq --set auth.username=admin,auth.password=admin bitnami/rabbitmq
# Проброс порта для настройки
kubectl port-forward --namespace otus-hw-2-volodina svc/otus-hw-rabbitmq 15672:15672
```

После запуска необходимо сделать настройки rabbitmq. 
А именно, создать exchange и binding

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

```
