# mqtt-mtls-latency-test

## Configurações iniciais

### Instalação do OpenVibe:
- Adicionar caixas CSV File Reader e LSL Export
- Ligar saídas rosas (output stream do CSV no input do LSL)

É preciso instalar a biblioteca do LSL:
- Clonar: https://github.com/sccn/liblsl
- Utilizar o script do repositório: `./standalone_compilation_linux.sh`
- Executar os comandos: `sudo cp liblsl.so /usr/local/lib/liblsl.so` e `sudo cp lslver /usr/local/lib/lslver`
- Por fim, exportar variável de ambiente do LSL: `export PYLSL_LIB=/usr/local/lib/liblsl.so`
