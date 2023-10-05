```
REST API com Flask

instalar dependencias: pip3 install -r requirements.txt   

executar código: python3 app.py

url utilizada: localhost:5001/users/
            ou 127.0.0.1:5001/users/

urls e métodos: 127.0.0.1:5001/ home
                127.0.0.1:5001/users/ sem funcionalidade, pagina de usuários
                127.0.0.1:5001/users/getAll/ retorna todos os usuários, metodo GET 
                127.0.0.1:5001/users/getByCpf/<string:cpf> retorna um usuário específico, metodo GET. (CPF é a chave primária)
                127.0.0.1:5001/users/create/ cria um usuário, metodo POST
                127.0.0.1:5001/users/manage/<string:cpf> atualiza um usuário, metodo PATCH ou DELETE

Todos os métodos que recebem paramêtros devem receber um objeto json.

ambiente de testes de requisição: Postman

Como banco de dados foi utilizado um arquivo chamado data.json, que contém um array de objetos JSON que são os registros de usuários
O programa tem rotinas que garantem a existência do arquivo e (parcialmente) sua usabilidade.

Durante o desenvolvimento, foi utilizado o nodemon para atualizar o servidor automaticamente, 
sem a necessidade de reiniciar o servidor a cada alteração no código. 
Para executar o servidor: nodemon --exec python3 app.py 
Para instalar as dependencias: npm i
Versão do node: 18.18.0

```

