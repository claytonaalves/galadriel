# encoding: utf8
import re

from pymongo import MongoClient
from bson.objectid import ObjectId

import calendar
from datetime import datetime, timedelta

client = MongoClient('10.1.1.100', 27017)
db = client.ello


def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def lower_case_underscore_to_camel_case(string):
    splitted_string = string.split('_')
    class_ = string.__class__
    return class_.join('', map(class_.capitalize, splitted_string[0:]))


class Excecao:

    def __init__(self, dados_excecao):
        self._excecao = dados_excecao

    @property
    def _id(self):
        return self._excecao['_id']

    @property
    def data(self):
        return utc_to_local(self._excecao['_id'].generation_time).strftime('%d/%m/%Y %H:%M:%S')

    @property
    def nome(self):
        return self._excecao['ExceptionName']

    @property
    def stacktrace(self):
        return self._excecao['StackTrace']

    @property
    def empresa(self):
        return self._excecao['Empresa']

    def __getattr__(self, attr):
        return self._excecao[lower_case_underscore_to_camel_case(attr)]

    @property
    def versao(self):
        """ Retorna a versão da estrutura do objeto Excecao
        """
        # Aqui vou considerar que se o objeto tiver o atributo System, a versão será a 2.
        # Posteriormente lembrar de adicionar um atributo Version para melhor identificar a versão.
        if self._excecao.get("System"):
            return 2
        else:
            return 1


def todas_excecoes(db, limit, offset):
    if offset>0:
        query = db.exceptions.find().sort('_id', -1).skip(offset).limit(limit)
    else:
        query = db.exceptions.find().sort('_id', -1).limit(10)
    for exc in query:
        yield Excecao(exc)


def todas_excecoes_por_cliente(db, matricula):
    for exc in db.exceptions.find({"Matricula": int(matricula)}).sort('_id', -1).limit(10):
        yield Excecao(exc)


def obtem_excecao(_id, db):
    exc = db.exceptions.find_one({"_id": ObjectId(_id)})
    return Excecao(exc)


if __name__ == "__main__":
    exc = obtem_excecao('5a4bf13aeadd47533767fc65', db)
    print(exc)

