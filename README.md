# Blaze Telegram

Este repositório é a implementação de um serviço onde você cria um grupo de telegram para enviar sinais de estratégias de entrada do jogo Double da Plataforma de apostas Blaze

## - Estrutura

Para este projeto, decidi usar eventos para facilitar a comunicação entre os módulos e pensando inclusive na comunicação de microserviços para caso modifique cada módulo para um serviço a parte da aplicação.

# Eventos:

Cada Handler apenas resolve o evento com seu nome igual, por tanto decidi criar cada handler para cada tipo de ação que será feita para cada exemplo.

## Tipos de Eventos:

- [ ] roullete-updated -> Evento para cada vez que a roleta da blaze atualizar
- [ ] double-signal-sended -> Evento para cada vez que um sinal for enviado
- [ ] double-result-sended -> Evento para cada vez que um resultado de sinal for enviado
