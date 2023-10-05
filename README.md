# Blaze Telegram

Este repositório é a implementação de um serviço onde você cria um grupo de telegram para enviar sinais de estratégias de entrada do jogo Double da Plataforma de apostas Blaze

## - Estrutura

Para este projeto, decidi usar eventos para facilitar a comunicação entre os módulos e pensando inclusive na comunicação de microserviços para caso modifique cada módulo para um serviço a parte da aplicação.

# Eventos:

Cada Handler apenas resolve o evento com seu nome igual, por tanto decidi criar cada handler para cada tipo de ação que será feita para cada exemplo.

## Tipos de Eventos:

- [x] roullete-updated -> Evento para cada vez que a roleta da blaze atualizar
- [x] double-signal-sended -> Evento para cada vez que um sinal for enviado
- [x] double-result-sended -> Evento para cada vez que um resultado de sinal for enviado
- [ ] data-updated -> Evento para cada vez que a roleta da casa de apostas atualizar

# Handlers:

- [x] roullete-updated -> Responsável por checar em cada estratégia se a roleta atual pode enviar um sinal ou resultado
- [x] double-signal-sended -> Este handler irá enviar uma mensagem para os grupos escolhidos com os sinais
- [ ] double-result-sended -> Irá enviar uma mensagem de resultado de sinais para os grupos escolhidos

# Serviços:

- [x] add-double -> Responsável em criar um evento de roullete-updated toda vez que consumir um novo dado.
- [x] create-strategy -> Cria uma estrategia com o tipo escolhido
- [x] transform_bet_to_msg -> Transforma uma aposta criada com a estratégia  em uma mensagem para ser mandada para o grupo
