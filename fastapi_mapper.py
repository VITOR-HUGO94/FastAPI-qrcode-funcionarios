import os

def mapear_projeto(caminho_base, arquivos_ignorados=None):
    if arquivos_ignorados is None:
        # Ignoramos pastas de ambiente virtual, git e caches
        arquivos_ignorados = ['.git', '__pycache__', '.env', 'venv', '.vscode', 'postgres_data']
    
    output_file = "contexto_projeto.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("ESTRUTURA E CONTEÚDO DO PROJETO FASTAPI\n")
        f.write("="*40 + "\n\n")
        
        for root, dirs, files in os.walk(caminho_base):
            # Filtra pastas ignoradas
            dirs[:] = [d for d in dirs if d not in arquivos_ignorados]
            
            nivel = root.replace(caminho_base, '').count(os.sep)
            indentacao = '  ' * nivel
            f.write(f'{indentacao}📁 {os.path.basename(root)}/\n')
            
            for file in files:
                # Ignorar arquivos binários ou pesados
                if file.endswith(('.py', '.yml', '.yaml', '.html', '.css', '.env', '.dockerignore', 'Dockerfile')):
                    f.write(f'{indentacao}  ├── 📄 {file}\n')
                    
                    caminho_completo = os.path.join(root, file)
                    try:
                        # O 'errors="ignore"' evita que o script trave se houver um caractere estranho
                        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as conteudo:
                            texto = conteudo.read()
                            f.write(f'\n{indentacao}  --- Início de {file} ---\n')
                            # Adiciona indentação ao conteúdo para ficar legível
                            conteudo_identado = "\n".join([f"{indentacao}  | {linha}" for linha in texto.splitlines()])
                            f.write(conteudo_identado)
                            f.write(f'\n{indentacao}  --- Fim de {file} ---\n\n')
                    except Exception as e:
                        f.write(f'{indentacao}  [Erro ao ler arquivo: {e}]\n')

    print(f"✅ Mapeamento concluído! Abra o arquivo '{output_file}' e copie o conteúdo para a IA.")

if __name__ == "__main__":
    mapear_projeto('.')