# Galadriel

Aplicação de controle de chamados e dashboard de monitoramento de uso.

## Ambiente de desenvolvimento

- Python 3.7+
- node/npm

### Ativar virtualenv e instalar dependências

```
$ python -m venv venv
$ venv/bin/activate
$ pip install -r requirements.txt
$ npm install
```

## Exportar imagem docker

```
$ docker save galadriel -o galadriel.container
```

## Importar imagem docker

```
$ docker load < galadriel.container
```

## Executar aplicação

```
docker run -d \
--name galadriel \
--restart always \
--env FIREBIRD_HOST=ip_do_servidor \
--env FIREBIRD_USER=sysdba \
--env FIREBIRD_PASSWORD=senha \
-p 5000:5000 \
galadriel
```
