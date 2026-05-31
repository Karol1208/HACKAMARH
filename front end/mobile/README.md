# Projeto Canindé: Guardião do Cerrado - Frontend (Mobile App)

Bem-vindo ao repositório do Aplicativo Mobile do **Projeto Canindé: Guardião do Cerrado**. Este aplicativo é fundamental para a atuação em campo (Eixo 2), permitindo a coleta de fotos georreferenciadas (RN01) e o escaneamento de mudas via Visão Computacional (RN05).

## Tecnologias e Stack
- **Flutter / Dart:** Framework multiplataforma utilizado para garantir alta performance e fluidez tanto em dispositivos Android quanto iOS.
- Integração nativa com recursos de câmera e GPS para extração de metadados EXIF.

## Como Iniciar o Sistema (Mobile) de Forma Profissional

Para configurar o ambiente e executar o aplicativo localmente, siga as instruções abaixo:

### 1. Pré-requisitos
- **Flutter SDK:** Certifique-se de ter a última versão estável instalada (veja [flutter.dev](https://flutter.dev/docs/get-started/install)).
- **Android Studio / Xcode:** Para emulação e compilação nativa (Android e iOS).
- Um dispositivo físico ou emulador configurado.

### 2. Configuração e Instalação
1. Abra o terminal na pasta do projeto mobile (`front end/mobile`).
2. Obtenha as dependências do projeto executando o comando:
   ```bash
   flutter pub get
   ```
3. Verifique se há problemas no ambiente executando:
   ```bash
   flutter doctor
   ```

### 3. Execução
Para iniciar o aplicativo no dispositivo/emulador conectado, execute:
```bash
flutter run
```

Para gerar a build de produção (APK/AAB):
```bash
flutter build apk --release
# ou para App Bundle
flutter build appbundle
```

---
**Equipe:** WB Projects Design & Dev
