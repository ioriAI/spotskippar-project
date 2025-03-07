# 🎵 SpotiSkipper

Um controlador Spotify elegante com interface gráfica moderna para gerenciar sua reprodução musical de forma divertida e eficiente.

## 🖥️ Requisitos do Sistema

- Windows 11
- Python 3.12 (recomendado instalar via Microsoft Store)
- Conta Spotify Premium
- Credenciais do Spotify Developer

## ✨ Funcionalidades

### 🎯 Principais Recursos
- **Timer Automático**: Contador regressivo de 90 segundos para cada música
- **Botão HELL YEAH!**: 
  - Curte a música atual (adiciona aos favoritos)
  - Mostra feedback visual com efeito verde
  - Pula automaticamente para a próxima música
- **Botão SKIP**: Pula diretamente para a próxima música
- **Interface Moderna**: Design inspirado no Spotify com tema escuro nativo

### 🎨 Elementos Visuais
- Contador regressivo grande e centralizado
- Indicador de músicas curtidas (❤️)
- Feedback visual ao curtir/pular músicas
- Efeitos de hover nos botões
- Timer fica vermelho nos últimos 10 segundos

## 🚀 Instalação e Uso

### Pré-requisitos
1. Instale o Python 3.12 da Microsoft Store
2. Obtenha suas credenciais do Spotify:
   - Acesse https://developer.spotify.com/dashboard
   - Crie um novo aplicativo
   - Configure a URI de redirecionamento como `http://localhost:8888/callback`
   - Copie o Client ID e Client Secret

### Configuração
1. Clone o repositório
2. Configure suas credenciais do Spotify:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha com suas credenciais:
   ```env
   SPOTIPY_CLIENT_ID=seu_client_id
   SPOTIPY_CLIENT_SECRET=seu_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

### Instalação de Dependências
```bash
python -m pip install -r requirements.txt
```

### Executando o Programa
```bash
python desktop/spotiskipper_desktop.py
```

Na primeira execução:
1. Uma janela do navegador abrirá automaticamente
2. Faça login na sua conta do Spotify
3. Autorize o aplicativo
4. Aproveite o SpotiSkipper!

## 🔧 Solução de Problemas

### Problemas de Autenticação Spotify
Se você encontrar erros de autenticação como "invalid_client":
1. Limpe os caches do Spotify:
   ```bash
   # Remova estes arquivos/diretórios se existirem
   ~/.cache/spotipy
   ./.cache
   ~/.spotipy/token
   .cache-[seu_client_id]
   ```
2. Verifique se as credenciais no arquivo `.env` correspondem exatamente às do Spotify Dashboard
3. No Spotify Dashboard, confirme:
   - O status do aplicativo está "Active"
   - A URI de redirecionamento está exatamente como `http://localhost:8888/callback`
   - Todas as permissões necessárias estão concedidas

### Interface Não Aparece
Se a interface estiver preta ou elementos não aparecerem:
1. Certifique-se de que está usando o Python 3.12 (recomendado)
2. Use um ambiente virtual limpo:
   ```bash
   python -m venv venv_new
   .\venv_new\Scripts\activate
   pip install -r requirements.txt
   ```
3. Instale o pacote pywin32:
   ```bash
   pip install pywin32
   ```

### Problemas com o Timer
Se o timer não estiver funcionando:
1. Verifique se o Spotify está aberto e tocando música
2. Confirme que você tem uma conta Spotify Premium
3. Verifique se todas as permissões foram aceitas na página de autorização do Spotify

### Logs de Depuração
Para diagnosticar problemas, você pode usar a versão de debug do aplicativo que mostra logs detalhados:
1. Use o arquivo `debug_spotiskipper.py`
2. Os logs mostrarão:
   - Status da inicialização
   - Erros de autenticação
   - Problemas de conexão com o Spotify
   - Estado da interface do usuário

### Permissões do Spotify
O aplicativo requer as seguintes permissões:
- user-read-playback-state
- user-modify-playback-state
- user-library-modify

Se alguma dessas permissões estiver faltando, você precisará reautorizar o aplicativo no Spotify Dashboard.

### Problemas Comuns
- **Erro "invalid_client"**: Geralmente resolvido limpando o cache e verificando as credenciais
- **Tela preta**: Resolvido reinstalando dependências em um ambiente virtual limpo
- **Música não pula**: Verifique se você tem Spotify Premium e se a música está tocando
- **Botões não funcionam**: Confirme que todas as permissões do Spotify foram concedidas

## 📝 Notas Importantes

- Na primeira execução, será necessário autorizar o aplicativo no Spotify
- Certifique-se de ter uma conexão ativa com a Internet
- Mantenha o Spotify aberto durante o uso do aplicativo
- A interface usa CustomTkinter para um visual moderno e elegante
- O tema escuro é ativado automaticamente

## 🤝 Contribuições

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para:
1. Abrir uma issue
2. Enviar um pull request
3. Sugerir novas funcionalidades