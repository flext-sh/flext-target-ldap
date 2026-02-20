# FLEXT Target LDAP

Singer Target para aplicacao de dados em destinos LDAP.

Descricao oficial atual: "FLEXT Target for LDAP directory loading".

## O que este projeto entrega

- Recebe stream Singer e grava em diretorio LDAP.
- Padroniza escrita/atualizacao de objetos de identidade.
- Apoia sincronizacao de dados de acesso em ambientes corporativos.

## Contexto operacional

- Entrada: registros Singer validados.
- Saida: diretorio LDAP atualizado.
- Dependencias: servidor LDAP e credenciais com permissao de escrita.

## Estado atual e risco de adocao

- Qualidade: **Alpha**
- Uso recomendado: **Nao produtivo**
- Nivel de estabilidade: em maturacao funcional e tecnica, sujeito a mudancas de contrato sem garantia de retrocompatibilidade.

## Diretriz para uso nesta fase

Aplicar este projeto somente em desenvolvimento, prova de conceito e homologacao controlada, com expectativa de ajustes frequentes ate maturidade de release.
