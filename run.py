from app import create_app, db
from app.models import Pessoa, Permissao, Endereco, Estabelecimento, Pagador, Pedido, Produto, Categoria, Consumo, Medida, Pix, Pagamento

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Pessoa': Pessoa, 'Permissao': Permissao, 'Endereco': Endereco, 'Estabelecimento': Estabelecimento, 'Pagador': Pagador, 'Pedido': Pedido, 'Produto': Produto, 'Categoria': Categoria, 'Consumo': Consumo, 'Medida': Medida, 'Pix': Pix, 'Pagamento': Pagamento}

if __name__ == '__main__':
    app.run(debug=True)
