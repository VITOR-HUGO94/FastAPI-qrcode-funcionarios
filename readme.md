# 🧾 Employee Management System (EMS)
### Backend Robusto com FastAPI • PostgreSQL • Docker • JWT • QR Code

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Modern%20API-009688?logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?style=flat"/>
  <img src="https://img.shields.io/badge/Auth-JWT-black?style=flat"/>
  <img src="https://img.shields.io/badge/Arquitetura-Clean%20Layered-orange?style=flat"/>
</p>

---

## 🎯 Visão Geral do Projeto

Este sistema de gestão de funcionários foi desenvolvido para simular um **ecossistema corporativo real**. Além das operações básicas de CRUD, o foco principal é a validação de identidade e certificação profissional através de perfis públicos acessíveis via **QR Code**.

O projeto utiliza **FastAPI** para alta performance e **Docker** para garantir um ambiente de desenvolvimento e produção isolado e consistente.

---

## 🚀 Funcionalidades Principais

* **Gestão de Funcionários:** Operações completas de CRUD.
* **Segurança Avançada:** Autenticação via JWT (JSON Web Tokens) com hashing de senhas via `bcrypt`.
* **Sistema de Arquivos:**
    * Upload de fotos de perfil (armazenadas como binário no banco).
    * Upload de certificados em PDF.
* **Validação via QR Code:** Geração automática de códigos que apontam para perfis públicos únicos baseados em UUID.
* **Infraestrutura:** Setup multi-container totalmente orquestrado via Docker Compose.
* **Health Check:** Endpoint dedicado para monitoramento do status da API.

---

## 🏗 Arquitetura do Sistema

O projeto segue uma estrutura de pastas organizada por responsabilidades (Clean Layered Architecture):

```text
backend/
├── app/
│   ├── auth.py         # Lógica de segurança e JWT
│   ├── crud.py         # Operações de banco de dados
│   ├── database.py     # Configuração do SQLAlchemy
│   ├── main.py         # Entrypoint do FastAPI
│   ├── models.py       # Modelos de dados (Tabelas)
│   ├── routes.py       # Definição dos endpoints
│   └── schemas.py      # Validação Pydantic
frontend/
└── templates/          # Páginas Jinja2 (Interface do usuário)
docker-compose.yml      # Orquestração de serviços

🐳 Como Executar com Docker
Certifique-se de ter o Docker instalado em sua máquina.

Suba os containers:

Bash
docker-compose up --build
Acesse a aplicação:

Interface Web: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

Verificação de Status: GET /health


## 🐳 Run with Docker

```bash
docker-compose up --build