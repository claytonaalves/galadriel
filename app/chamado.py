import fdb

def lista_de_chamados():
    con = fdb.connect(host='10.1.1.100', user='sysdba', password='!3ll0tec', database='ello')
    
    q = con.cursor()
    
    q.execute('Select IdSolicitacao, Descricao From TSolSolicitacao Where Situacao = 1')
    chamados = q.fetchall()
    return chamados