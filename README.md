#### Ambiente de Desenvolvimento para Microsserviços

Este repositório serve como base para a criação de um ambiente de desenvolvimento centrado em microsserviços.
A estrutura fornecida suporta diversos componentes backend, como Lambdas, APIs, e outros serviços que podem ser integrados harmoniosamente com as ferramentas da AWS.

#### Estrutura do Projeto

A estrutura do projeto é projetada para oferecer flexibilidade e modularidade, facilitando a incorporação de microsserviços independentes.
O diretório principal pode conter subdiretórios para diferentes serviços ou componentes.


* src: O diretório principal para o código-fonte da aplicação.
* function_lambda: Contém o código para a função Lambda 1.
* function_lambda2: Contém o código para a função Lambda 2.
* api: Diretório para o código relacionado à API.
* common: Contém código e recursos compartilhados entre diferentes partes do projeto.
* infra: Código e scripts relacionados à infraestrutura, como configurações do AWS CloudFormation ou scripts de automação.
* README.md: Este arquivo fornece uma visão geral da estrutura do projeto.
* .gitignore: Arquivo de configuração do Git para especificar quais arquivos e diretórios devem ser ignorados pelo controle de versão.
* tests: Diretório para testes automatizados.
* ...: Outros arquivos e diretórios necessários para o funcionamento ou desenvolvimento do projeto.
  
#### Configuração do Projeto
1. AWS Configuration:

* Certifique-se de configurar suas credenciais AWS e ajustar as configurações necessárias para interagir com os serviços da AWS.
  
2. Configuração dos Componentes:
   
* Dentro de cada diretório (function_lambda, api, etc.), forneça instruções claras sobre como configurar e executar os componentes específicos..

