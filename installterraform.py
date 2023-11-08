import os
import platform
import requests
import zipfile
import tempfile
import shutil
import sys

# Verifique o sistema operacional
system = platform.system()
if system == 'Windows':
    platform = 'windows_amd64'
elif system == 'Linux':
    platform = 'linux_amd64'
else:
    print("Sistema operacional não suportado.")
    sys.exit(1)

# Verifique a versão mais recente do Terraform
try:
    response = requests.get("https://releases.hashicorp.com/terraform/index.json")
    data = response.json()
    latest_version = data['versions'][0]['version']
except Exception as e:
    print(f"Erro ao buscar a versão mais recente do Terraform: {e}")
    sys.exit(1)

# Diretório temporário para download e extração
temp_dir = tempfile.mkdtemp()

# URL de download do Terraform
download_url = f"https://releases.hashicorp.com/terraform/{latest_version}/terraform_{latest_version}_{platform}.zip"

# Faça o download do Terraform
try:
    download_response = requests.get(download_url)
    if download_response.status_code == 200:
        with open(os.path.join(temp_dir, 'terraform.zip'), 'wb') as f:
            f.write(download_response.content)
    else:
        print(f"Erro ao fazer o download do Terraform. Código de status: {download_response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"Erro ao fazer o download do Terraform: {e}")
    sys.exit(1)

# Extraia o Terraform
try:
    with zipfile.ZipFile(os.path.join(temp_dir, 'terraform.zip'), 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
except Exception as e:
    print(f"Erro ao extrair o Terraform: {e}")
    sys.exit(1)

# Mova o executável do Terraform para um diretório no seu PATH
try:
    terraform_dir = os.path.join(temp_dir, 'terraform')
    if system == 'Windows':
        terraform_exe = os.path.join(temp_dir, 'terraform.exe')
        shutil.move(terraform_exe, os.path.join(os.environ['SystemRoot'], 'System32'))
    else:
        shutil.move(terraform_dir, '/usr/local/bin')
    print("Terraform instalado com sucesso.")
except Exception as e:
    print(f"Erro ao mover o Terraform para o diretório do sistema: {e}")
    sys.exit(1)

# Limpeza do diretório temporário
shutil.rmtree(temp_dir)

# Verifique a instalação do Terraform
try:
    check_output = os.popen("terraform --version").read()
    print(check_output)
except Exception as e:
    print(f"Erro ao verificar a instalação do Terraform: {e}")

print("Instalação concluída com sucesso.")
