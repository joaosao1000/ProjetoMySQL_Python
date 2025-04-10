import mysql.connector
from mysql.connector import Error


# Função para conectar ao banco de dados
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="2553",
            database="trabalho"
        )
        print("Conexão ao MySQL bem-sucedida")
        return connection
    except Error as e:
        print(f"O erro '{e}' ocorreu")
        return None


# INSERIR PRODUTOS
def insert_product(connection):
    nome = input("Nome do produto: ")
    peso = float(input("Peso do produto: "))
    quantidade = int(input("Quantidade: "))
    quantidade_minima = int(input("Quantidade mínima: "))
    categoria_id = int(input("ID da categoria: "))
    fornecedor_id = int(input("ID do fornecedor: "))
    preco_fornecedor = float(input("Preço de compra do fornecedor: "))

    cursor = connection.cursor()
    query_produto = """
    INSERT INTO Produtos (nome, peso, quantidade, quantidade_minima, categoria_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query_produto, (nome, peso, quantidade, quantidade_minima, categoria_id))
    produto_id = cursor.lastrowid

    query_fornecedor = """
    INSERT INTO Produto_Fornecedores (produto_id, fornecedor_id, preco_fornecedor)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query_fornecedor, (produto_id, fornecedor_id, preco_fornecedor))

    connection.commit()
    print("Produto inserido com sucesso!")


# LISTAR PRODUTOS
def view_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT p.id, p.nome, p.peso, p.quantidade, p.quantidade_minima, c.nome AS categoria, f.nome AS fornecedor, pf.preco_fornecedor
    FROM Produtos p
    JOIN Categorias c ON p.categoria_id = c.id
    LEFT JOIN Produto_Fornecedores pf ON p.id = pf.produto_id
    LEFT JOIN Fornecedores f ON pf.fornecedor_id = f.id
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    for produto in produtos:
        print(
            f"ID: {produto[0]}, Nome: {produto[1]}, Peso: {produto[2]}, Quantidade: {produto[3]}, Quantidade Mínima: {produto[4]}, Categoria: {produto[5]}, Fornecedor: {produto[6]}, Preço do Fornecedor: {produto[7]}")


# PRODUTOS COM ESTOQUE BAIXO
def view_low_stock_products(connection):
    cursor = connection.cursor()

    query = """
    SELECT id, nome, quantidade, quantidade_minima
    FROM Produtos
    WHERE quantidade <= quantidade_minima
    ORDER BY quantidade ASC
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    if produtos:
        print("\nProdutos com quantidade em estoque menor ou igual à quantidade mínima requerida:")
        for produto in produtos:
            print(
                f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade em Estoque: {produto[2]}, Quantidade Mínima: {produto[3]}")
    else:
        print("\nTodos os produtos estão com quantidade em estoque acima da quantidade mínima requerida.")


# DELETAR PRODUTOS
def delete_product(connection):
    produto_id = int(input("Digite o ID do produto que deseja excluir: "))

    cursor = connection.cursor()

    query_check = """
    SELECT COUNT(*) FROM Entradas WHERE produto_id = %s
    UNION ALL
    SELECT COUNT(*) FROM Saida_Produtos WHERE produto_id = %s
    """
    cursor.execute(query_check, (produto_id, produto_id))
    result = cursor.fetchall()

    if result[0][0] == 0 and result[1][0] == 0:
        query_delete = "DELETE FROM Produtos WHERE id = %s"
        cursor.execute(query_delete, (produto_id,))
        connection.commit()
        print("Produto excluído com sucesso!")
    else:
        print("Não é possível excluir o produto, pois ele está associado a uma entrada ou saída.")


# INSERIR FORNECEDOR
def insert_supplier(connection):
    nome = input("Nome do fornecedor: ")
    contato = input("Contato do fornecedor: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Fornecedores (nome, contato) 
    VALUES (%s, %s)
    """
    cursor.execute(query, (nome, contato))
    connection.commit()
    print("Fornecedor inserido com sucesso!")


# VER FORNECEDORES
def view_suppliers(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Fornecedores"
    cursor.execute(query)
    fornecedores = cursor.fetchall()

    for fornecedor in fornecedores:
        print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Contato: {fornecedor[2]}")


# VER PRODUTOS POR FORNECEDORES
def view_products_by_supplier(connection):
    fornecedor_id = int(input("Digite o ID do fornecedor para visualizar seus produtos: "))

    cursor = connection.cursor()
    query = """
    SELECT p.id AS produto_id, p.nome AS produto, p.quantidade, p.quantidade_minima, pf.preco_fornecedor
    FROM Produto_Fornecedores pf
    JOIN Produtos p ON pf.produto_id = p.id
    WHERE pf.fornecedor_id = %s
    ORDER BY p.nome
    """
    cursor.execute(query, (fornecedor_id,))
    produtos = cursor.fetchall()

    if produtos:
        print(f"\nProdutos do fornecedor ID {fornecedor_id}:")
        for produto in produtos:
            print(
                f"  ID Produto: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Quantidade Mínima: {produto[3]}, Preço do Fornecedor: {produto[4]}")
    else:
        print(f"Nenhum produto encontrado para o fornecedor ID {fornecedor_id}.")


# EXCLUIR FORBECEDOR QUE NÃO ESTEJA ASSOCIADO A UM PRODUTO
def delete_supplier(connection):
    fornecedor_id = int(input("Digite o ID do fornecedor que deseja excluir: "))

    cursor = connection.cursor()

    query_check = """
    SELECT COUNT(*) FROM Produto_Fornecedores WHERE fornecedor_id = %s
    """
    cursor.execute(query_check, (fornecedor_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        query_delete = "DELETE FROM Fornecedores WHERE id = %s"
        cursor.execute(query_delete, (fornecedor_id,))
        connection.commit()
        print("Fornecedor excluído com sucesso!")
    else:
        print("Não é possível excluir o fornecedor, pois ele está associado a um ou mais produtos.")


# INSERIR TRANSPORTADORAS
def insert_transporter(connection):
    nome = input("Nome da transportadora: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Transportadoras (nome) 
    VALUES (%s)
    """
    cursor.execute(query, (nome,))
    connection.commit()
    print("Transportadora inserida com sucesso!")


# LISTAR TRANSPORTADORAS
def view_transporters(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Transportadoras"
    cursor.execute(query)
    transportadoras = cursor.fetchall()

    for transportadora in transportadoras:
        print(f"ID: {transportadora[0]}, Nome: {transportadora[1]}")


# DELETAR TRANSPORTADORA QUE NÃO ESTEJA ASSOCIADA A UMA SAIDA OU ENTRADA
def delete_transporter(connection):
    transportadora_id = int(input("Digite o ID da transportadora que deseja excluir: "))

    cursor = connection.cursor()

    query_check = """
    SELECT COUNT(*) FROM Entradas WHERE transportadora_id = %s
    UNION ALL
    SELECT COUNT(*) FROM Saidas WHERE transportadora_id = %s
    """
    cursor.execute(query_check, (transportadora_id, transportadora_id))
    result = cursor.fetchall()

    if result[0][0] == 0 and result[1][0] == 0:
        query_delete = "DELETE FROM Transportadoras WHERE id = %s"
        cursor.execute(query_delete, (transportadora_id,))
        connection.commit()
        print("Transportadora excluída com sucesso!")
    else:
        print("Não é possível excluir a transportadora, pois ela está associada a uma entrada ou saída.")


# INSERIR CATEGORIAS
def insert_category(connection):
    nome = input("Nome da categoria: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Categorias (nome) 
    VALUES (%s)
    """
    cursor.execute(query, (nome,))
    connection.commit()
    print("Categoria inserida com sucesso!")


# LISTAR CATEGORIAS
def view_categories(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Categorias"
    cursor.execute(query)
    categorias = cursor.fetchall()

    for categoria in categorias:
        print(f"ID: {categoria[0]}, Nome: {categoria[1]}")


# ORDENA AS CATEGORIAS COM MAIS ITENS
def view_category_with_most_items(connection):
    cursor = connection.cursor()

    query = """
    SELECT c.nome AS categoria, SUM(p.quantidade) AS total_itens
    FROM Categorias c
    JOIN Produtos p ON c.id = p.categoria_id
    GROUP BY c.id
    ORDER BY total_itens DESC
    LIMIT 1
    """
    cursor.execute(query)
    resultado = cursor.fetchone()

    if resultado:
        print(f"\nCategoria com mais itens em estoque: {resultado[0]} com {resultado[1]} itens")
    else:
        print("Nenhum item encontrado nas categorias.")


# DELETAR CATEGORIA QUE NÃO TENHA PRODUTO ASSOCIADO A ELA
def delete_category(connection):
    categoria_id = int(input("Digite o ID da categoria que deseja excluir: "))

    cursor = connection.cursor()

    query_check = """
    SELECT COUNT(*) FROM Produtos WHERE categoria_id = %s
    """
    cursor.execute(query_check, (categoria_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        query_delete = "DELETE FROM Categorias WHERE id = %s"
        cursor.execute(query_delete, (categoria_id,))
        connection.commit()
        print("Categoria excluída com sucesso!")
    else:
        print("Não é possível excluir a categoria, pois ela está associada a um ou mais produtos.")


# FUNÇÕES DE ENTRADA E SAIDA
def register_product_entry(connection):
    produto_id = int(input("ID do produto: "))
    data_pedido = input("Data do pedido (AAAA-MM-DD): ")
    data_entrega = input("Data da entrega (AAAA-MM-DD): ")
    quantidade = int(input("Quantidade: "))
    peso_total = float(input("Peso total: "))
    transportadora_id = int(input("ID da transportadora: "))

    cursor = connection.cursor()
    query = """
    INSERT INTO Entradas (produto_id, data_pedido, data_entrega, quantidade, peso_total, transportadora_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (produto_id, data_pedido, data_entrega, quantidade, peso_total, transportadora_id))
    connection.commit()
    print("Entrada registrada com sucesso!")


def register_product_exit(connection):
    data_saida = input("Data de saída (AAAA-MM-DD): ")
    loja = input("Nome da loja: ")
    peso_total = float(input("Peso total: "))
    transportadora_id = int(input("ID da transportadora: "))

    cursor = connection.cursor()
    query = """
    INSERT INTO Saidas (data_saida, loja, peso_total, transportadora_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (data_saida, loja, peso_total, transportadora_id))
    saida_id = cursor.lastrowid

    while True:
        produto_id = int(input("ID do produto: "))
        quantidade = int(input("Quantidade: "))
        preco_venda = float(input("Preço de venda: "))

        query = """
        INSERT INTO Saida_Produtos (saida_id, produto_id, quantidade, preco_venda)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (saida_id, produto_id, quantidade, preco_venda))

        more = input("Adicionar mais produtos a esta saída? (s/n): ")
        if more.lower() != 's':
            break

    connection.commit()
    print("Saída registrada com sucesso!")


# LISTAR ENTRADAS E SAIDAS
def view_entries(connection):
    cursor = connection.cursor()
    query = """
    SELECT e.id, p.nome AS produto, e.data_pedido, e.data_entrega, e.quantidade, e.peso_total, t.nome AS transportadora,
           DATEDIFF(e.data_entrega, e.data_pedido) AS tempo_entrega
    FROM Entradas e
    JOIN Produtos p ON e.produto_id = p.id
    JOIN Transportadoras t ON e.transportadora_id = t.id
    ORDER BY e.data_entrega ASC
    """
    cursor.execute(query)
    entradas = cursor.fetchall()

    for entrada in entradas:
        print(
            f"ID: {entrada[0]}, Produto: {entrada[1]}, Data do Pedido: {entrada[2]}, Data de Entrega: {entrada[3]}, Tempo de Entrega: {entrada[7]} dias, Quantidade: {entrada[4]}, Peso Total: {entrada[5]}, Transportadora: {entrada[6]}")


def view_exits(connection):
    cursor = connection.cursor()
    query = """
    SELECT s.id, sp.produto_id, p.nome AS produto, sp.quantidade, sp.preco_venda, s.data_saida, s.loja, s.peso_total, t.nome AS transportadora
    FROM Saidas s
    JOIN Saida_Produtos sp ON s.id = sp.saida_id
    JOIN Produtos p ON sp.produto_id = p.id
    JOIN Transportadoras t ON s.transportadora_id = t.id
    ORDER BY s.data_saida ASC
    """
    cursor.execute(query)
    saidas = cursor.fetchall()

    for saida in saidas:
        print(
            f"ID: {saida[0]}, Produto: {saida[2]}, Quantidade: {saida[3]}, Preço de Venda: {saida[4]}, Data de Saída: {saida[5]}, Loja: {saida[6]}, Peso Total: {saida[7]}, Transportadora: {saida[8]}")


# LISTAR HISTÓRICO DE PRODUTOS
def view_product_history(connection):
    produto_id = int(input("Digite o ID do produto para visualizar o histórico completo: "))

    cursor = connection.cursor()

    # Consultar Entradas do Produto
    query_entradas = """
    SELECT e.data_pedido, e.data_entrega, e.quantidade, e.peso_total, t.nome AS transportadora,
           DATEDIFF(e.data_entrega, e.data_pedido) AS tempo_entrega
    FROM Entradas e
    JOIN Transportadoras t ON e.transportadora_id = t.id
    WHERE e.produto_id = %s
    ORDER BY e.data_entrega ASC
    """
    cursor.execute(query_entradas, (produto_id,))
    entradas = cursor.fetchall()

    # Consultar Saídas do Produto
    query_saidas = """
    SELECT s.data_saida, sp.quantidade, sp.preco_venda, s.loja, s.peso_total, t.nome AS transportadora
    FROM Saidas s
    JOIN Saida_Produtos sp ON s.id = sp.saida_id
    JOIN Transportadoras t ON s.transportadora_id = t.id
    WHERE sp.produto_id = %s
    ORDER BY s.data_saida ASC
    """
    cursor.execute(query_saidas, (produto_id,))
    saidas = cursor.fetchall()

    # Exibir Histórico
    print(f"\nHistórico completo do Produto ID {produto_id}:")
    print("\nEntradas:")
    if entradas:
        for entrada in entradas:
            print(
                f"  Data do Pedido: {entrada[0]}, Data de Entrega: {entrada[1]}, Tempo de Entrega: {entrada[5]} dias, Quantidade: {entrada[2]}, Peso Total: {entrada[3]}, Transportadora: {entrada[4]}")
    else:
        print("  Nenhuma entrada registrada.")

    print("\nSaídas:")
    if saidas:
        for saida in saidas:
            print(
                f"  Data de Saída: {saida[0]}, Quantidade: {saida[1]}, Preço de Venda: {saida[2]}, Loja: {saida[3]}, Peso Total: {saida[4]}, Transportadora: {saida[5]}")
    else:
        print("  Nenhuma saída registrada.")


# FATURAMENTO POR LOJA
def calculate_revenue_by_store(connection):
    month = input("Digite o mês para calcular o faturamento (formato MM): ")
    year = input("Digite o ano para calcular o faturamento (formato YYYY): ")

    cursor = connection.cursor()

    query = """
    SELECT s.loja, SUM(sp.quantidade * sp.preco_venda) AS total_vendas
    FROM Saidas s
    JOIN Saida_Produtos sp ON s.id = sp.saida_id
    WHERE MONTH(s.data_saida) = %s AND YEAR(s.data_saida) = %s
    GROUP BY s.loja
    ORDER BY total_vendas DESC
    """
    cursor.execute(query, (month, year))
    resultados = cursor.fetchall()

    if resultados:
        print(f"\nFaturamento por loja no mês {month}/{year}:")
        for loja, total_vendas in resultados:
            print(f"Loja: {loja}, Faturamento: R${total_vendas:.2f}")

        # Identificar a loja com maior faturamento
        loja_mais_vendas = resultados[0]
        print(f"\nLoja com maior faturamento: {loja_mais_vendas[0]} com R${loja_mais_vendas[1]:.2f}")
    else:
        print(f"Nenhuma venda registrada no mês {month}/{year}.")


# INFORMAÇÕES EXTRAS
def view_top_stock_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT nome, quantidade
    FROM Produtos
    ORDER BY quantidade DESC
    LIMIT 10;
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    print("\nProdutos com maior quantidade em estoque:")
    for produto in produtos:
        print(f"Nome: {produto[0]}, Quantidade: {produto[1]}")


def view_most_valuable_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT nome, quantidade, preco_unitario, (quantidade * preco_unitario) AS valor_total
    FROM Produtos
    ORDER BY valor_total DESC
    LIMIT 10;
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    print("\nProdutos com o maior valor total em estoque:")
    for produto in produtos:
        print(f"Nome: {produto[0]}, Quantidade: {produto[1]}, Preço Unitário: {produto[2]}, Valor Total: {produto[3]}")


def view_most_used_transporter(connection):
    cursor = connection.cursor()
    query = """
    SELECT t.nome, COUNT(*) AS total_usos
    FROM Transportadoras t
    JOIN (
        SELECT transportadora_id FROM Entradas
        UNION ALL
        SELECT transportadora_id FROM Saidas
    ) as usos ON t.id = usos.transportadora_id
    GROUP BY t.nome
    ORDER BY total_usos DESC
    LIMIT 1;
    """
    cursor.execute(query)
    transportadora = cursor.fetchone()

    print(f"\nTransportadora mais utilizada: {transportadora[0]} com {transportadora[1]} usos.")


def view_never_sold_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT p.nome
    FROM Produtos p
    LEFT JOIN Saida_Produtos sp ON p.id = sp.produto_id
    WHERE sp.produto_id IS NULL;
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    print("\nProdutos que nunca foram vendidos:")
    for produto in produtos:
        print(f"Nome: {produto[0]}")


def view_top_supplier(connection):
    cursor = connection.cursor()
    query = """
    SELECT f.nome, COUNT(pf.produto_id) AS total_produtos
    FROM Fornecedores f
    JOIN Produto_Fornecedores pf ON f.id = pf.fornecedor_id
    GROUP BY f.nome
    ORDER BY total_produtos DESC
    LIMIT 1;
    """
    cursor.execute(query)
    fornecedor = cursor.fetchone()

    print(f"\nFornecedor com o maior número de produtos fornecidos: {fornecedor[0]} com {fornecedor[1]} produtos.")


def view_total_spent_by_supplier(connection):
    cursor = connection.cursor()
    query = """
    SELECT f.nome, SUM(pf.preco_fornecedor * p.quantidade) AS total_gasto
    FROM Fornecedores f
    JOIN Produto_Fornecedores pf ON f.id = pf.fornecedor_id
    JOIN Produtos p ON pf.produto_id = p.id
    GROUP BY f.nome
    ORDER BY total_gasto DESC;
    """
    cursor.execute(query)
    fornecedores = cursor.fetchall()

    print("\nValor total gasto em produtos de cada fornecedor:")
    for fornecedor in fornecedores:
        print(f"Fornecedor: {fornecedor[0]}, Total Gasto: R${fornecedor[1]:.2f}")


def view_near_min_stock_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT nome, quantidade, quantidade_minima
    FROM Produtos
    WHERE quantidade <= quantidade_minima + 10
    ORDER BY quantidade ASC;
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    print("\nProdutos que estão prestes a atingir o estoque mínimo:")
    for produto in produtos:
        print(f"Nome: {produto[0]}, Quantidade: {produto[1]}, Quantidade Mínima: {produto[2]}")


def view_sales_by_category(connection):
    cursor = connection.cursor()
    query = """
    SELECT c.nome AS categoria, SUM(sp.quantidade * sp.preco_venda) AS total_vendas
    FROM Categorias c
    JOIN Produtos p ON c.id = p.categoria_id
    JOIN Saida_Produtos sp ON p.id = sp.produto_id
    GROUP BY c.nome
    ORDER BY total_vendas DESC;
    """
    cursor.execute(query)
    categorias = cursor.fetchall()

    print("\nVendas totais por categoria:")
    for categoria in categorias:
        print(f"Categoria: {categoria[0]}, Total Vendas: R${categoria[1]:.2f}")


def view_avg_delivery_time_by_transporter(connection):
    cursor = connection.cursor()
    query = """
    SELECT t.nome, AVG(DATEDIFF(e.data_entrega, e.data_pedido)) AS tempo_medio_entrega
    FROM Transportadoras t
    JOIN Entradas e ON t.id = e.transportadora_id
    GROUP BY t.nome
    ORDER BY tempo_medio_entrega ASC;
    """
    cursor.execute(query)
    transportadoras = cursor.fetchall()

    print("\nMédia de tempo de entrega por transportadora:")
    for transportadora in transportadoras:
        print(f"Transportadora: {transportadora[0]}, Tempo Médio de Entrega: {transportadora[1]:.2f} dias")


def view_top_entrance_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT p.nome, COUNT(e.id) AS total_entradas
    FROM Produtos p
    JOIN Entradas e ON p.id = e.produto_id
    GROUP BY p.nome
    ORDER BY total_entradas DESC
    LIMIT 10;
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    print("\nProdutos com maior número de entradas:")
    for produto in produtos:
        print(f"Nome: {produto[0]}, Total Entradas: {produto[1]}")


# Menus
def main_menu():
    print("\nMenu Principal")
    print("1. Gerenciar Produtos")
    print("2. Gerenciar Fornecedores")
    print("3. Gerenciar Transportadoras")
    print("4. Gerenciar Categorias")
    print("5. Registrar Entrada de Produto")
    print("6. Registrar Saída de Produto")
    print("7. Visualizar Entradas")
    print("8. Visualizar Saídas")
    print("9. Visualizar Histórico de Produto")
    print("10. Calcular Faturamento por Loja")
    print("11. Informações Extras")
    print("12. Sair")


def product_menu():
    print("\nMenu de Produtos")
    print("1. Inserir novo produto")
    print("2. Visualizar todos os produtos")
    print("3. Visualizar produtos com estoque baixo")
    print("4. Excluir produto")
    print("5. Voltar ao Menu Principal")


def supplier_menu():
    print("\nMenu de Fornecedores")
    print("1. Inserir novo fornecedor")
    print("2. Visualizar todos os fornecedores")
    print("3. Visualizar produtos por fornecedor")
    print("4. Excluir fornecedor")
    print("5. Voltar ao Menu Principal")


def transporter_menu():
    print("\nMenu de Transportadoras")
    print("1. Inserir nova transportadora")
    print("2. Visualizar todas as transportadoras")
    print("3. Excluir transportadora")
    print("4. Voltar ao Menu Principal")


def category_menu():
    print("\nMenu de Categorias")
    print("1. Inserir nova categoria")
    print("2. Visualizar todas as categorias")
    print("3. Ver categoria com mais itens em estoque")
    print("4. Excluir categoria")
    print("5. Voltar ao Menu Principal")


def extra_info_menu():
    print("\nMenu de Informações Extras")
    print("1. Produtos com maior quantidade em estoque")
    print("2. Produtos com o maior valor total em estoque")
    print("3. Transportadora mais utilizada")
    print("4. Produtos que nunca foram vendidos")
    print("5. Fornecedor com o maior número de produtos fornecidos")
    print("6. Valor total gasto em produtos de cada fornecedor")
    print("7. Produtos que estão prestes a atingir o estoque mínimo")
    print("8. Vendas totais por categoria")
    print("9. Média de tempo de entrega por transportadora")
    print("10. Produtos com maior número de entradas")
    print("11. Voltar ao Menu Principal")


def main():
    connection = create_connection()
    if connection is None:
        return

    while True:
        main_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            while True:
                product_menu()
                product_choice = input("Escolha uma opção: ")
                if product_choice == '1':
                    insert_product(connection)
                elif product_choice == '2':
                    view_products(connection)
                elif product_choice == '3':
                    view_low_stock_products(connection)
                elif product_choice == '4':
                    delete_product(connection)
                elif product_choice == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '2':
            while True:
                supplier_menu()
                supplier_choice = input("Escolha uma opção: ")
                if supplier_choice == '1':
                    insert_supplier(connection)
                elif supplier_choice == '2':
                    view_suppliers(connection)
                elif supplier_choice == '3':
                    view_products_by_supplier(connection)
                elif supplier_choice == '4':
                    delete_supplier(connection)
                elif supplier_choice == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '3':
            while True:
                transporter_menu()
                transporter_choice = input("Escolha uma opção: ")
                if transporter_choice == '1':
                    insert_transporter(connection)
                elif transporter_choice == '2':
                    view_transporters(connection)
                elif transporter_choice == '3':
                    delete_transporter(connection)
                elif transporter_choice == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '4':
            while True:
                category_menu()
                category_choice = input("Escolha uma opção: ")
                if category_choice == '1':
                    insert_category(connection)
                elif category_choice == '2':
                    view_categories(connection)
                elif category_choice == '3':
                    view_category_with_most_items(connection)
                elif category_choice == '4':
                    delete_category(connection)
                elif category_choice == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '5':
            register_product_entry(connection)

        elif choice == '6':
            register_product_exit(connection)

        elif choice == '7':
            view_entries(connection)

        elif choice == '8':
            view_exits(connection)

        elif choice == '9':
            view_product_history(connection)

        elif choice == '10':
            calculate_revenue_by_store(connection)

        elif choice == '11':
            while True:
                extra_info_menu()
                info_choice = input("Escolha uma opção: ")
                if info_choice == '1':
                    view_top_stock_products(connection)
                elif info_choice == '2':
                    view_most_valuable_products(connection)
                elif info_choice == '3':
                    view_most_used_transporter(connection)
                elif info_choice == '4':
                    view_never_sold_products(connection)
                elif info_choice == '5':
                    view_top_supplier(connection)
                elif info_choice == '6':
                    view_total_spent_by_supplier(connection)
                elif info_choice == '7':
                    view_near_min_stock_products(connection)
                elif info_choice == '8':
                    view_sales_by_category(connection)
                elif info_choice == '9':
                    view_avg_delivery_time_by_transporter(connection)
                elif info_choice == '10':
                    view_top_entrance_products(connection)
                elif info_choice == '11':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '12':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    connection.close()


if __name__ == "__main__":
    main()
