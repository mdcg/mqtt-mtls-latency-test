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

### Configurando MQTT e InfluxDB:

- Configurar AVAHI para disponibilizar um domain name para a máquina local: https://pi3g.com/avahi-how-to-assign-several-local-names-to-same-ip/

- Executar: `docker-compose up`